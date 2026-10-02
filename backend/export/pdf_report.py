"""PDF academic report generation using ReportLab (no external system dependencies)."""
from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO

from backend.config import SCORING_YAML
from backend.db import models
from backend.db.session import SessionLocal
from backend.scoring.scoring import load_config
from backend.statistics.statistics import compute_statistics


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _esc(text: str | None) -> str:
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _score_dim(scores, name):
    for s in scores:
        if s.dimension == name:
            return s
    return None


def generate_pdf_report(comparison_id: int) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors

    with SessionLocal() as session:
        comparison = session.get(models.Comparison, comparison_id)
        if not comparison:
            raise ValueError("Comparison not found.")
        problem = session.get(models.Problem, comparison.problem_id)
        cfg = load_config()

        ai_er = session.query(models.ExecutionResult).filter_by(
            comparison_id=comparison_id, code_variant="AI").first()
        hu_er = session.query(models.ExecutionResult).filter_by(
            comparison_id=comparison_id, code_variant="HUMAN").first()
        ai_scores = session.query(models.Score).filter_by(
            comparison_id=comparison_id, code_variant="AI").all()
        hu_scores = session.query(models.Score).filter_by(
            comparison_id=comparison_id, code_variant="HUMAN").all()
        ai_sec = session.query(models.SecurityFinding).filter_by(
            comparison_id=comparison_id, code_variant="AI").all()
        hu_sec = session.query(models.SecurityFinding).filter_by(
            comparison_id=comparison_id, code_variant="HUMAN").all()
        ai_static = session.query(models.StaticAnalysisResult).filter_by(
            comparison_id=comparison_id, code_variant="AI").all()
        hu_static = session.query(models.StaticAnalysisResult).filter_by(
            comparison_id=comparison_id, code_variant="HUMAN").all()
        comp_rows = session.query(models.ComparisonResult).filter_by(
            comparison_id=comparison_id).all()
        stats = compute_statistics(session, cfg)

        ai_complexity = {r.metric_name: r.raw_value for r in session.query(models.ComplexityData).filter_by(
            comparison_id=comparison_id, code_variant="AI").all()}
        hu_complexity = {r.metric_name: r.raw_value for r in session.query(models.ComplexityData).filter_by(
            comparison_id=comparison_id, code_variant="HUMAN").all()}

        ai_quality = [f for f in ai_static if f.category == "code_quality"]
        hu_quality = [f for f in hu_static if f.category == "code_quality"]

        ai_overall = next((s.overall_score for s in ai_scores if s.overall_score is not None), None)
        hu_overall = next((s.overall_score for s in hu_scores if s.overall_score is not None), None)

        dims = ["reliability", "performance", "maintainability", "security", "complexity", "code_quality"]
        ai_dim = {d: _score_dim(ai_scores, d) for d in dims}
        hu_dim = {d: _score_dim(hu_scores, d) for d in dims}
        weights = {d["name"]: d["weight"] for d in cfg["overall_score"]["dimensions"]}

        title = _esc(problem.title) if problem else 'N/A'
        category = _esc(problem.category) if problem else 'N/A'
        difficulty = _esc(problem.difficulty) if problem else 'N/A'
        desc = _esc(problem.description) if problem else 'N/A'
        ai_name = _esc(comparison.ai_name)
        status = _esc(comparison.status)
        created = _esc(comparison.created_at.isoformat() if comparison.created_at else None)
        completed = _esc(comparison.completed_at.isoformat() if comparison.completed_at else None)
        timeout = cfg.get('execution', {}).get('timeout_seconds', 10)
        alpha = cfg.get('statistics', {}).get('alpha', 0.05)
        neutral = cfg.get('normalization', {}).get('neutral_value', 50)
        ai_code = _esc(comparison.ai_source_code)
        hu_code = _esc(comparison.human_source_code)
        problem_version = comparison.problem_version if comparison.problem_version is not None else 'N/A'
        test_case_version = comparison.test_case_version if comparison.test_case_version is not None else 'N/A'

        preflight_ai = session.query(models.PreflightResult).filter_by(
            comparison_id=comparison_id, code_variant="AI").all()
        preflight_human = session.query(models.PreflightResult).filter_by(
            comparison_id=comparison_id, code_variant="HUMAN").all()

        ai_status = ai_er.execution_status if ai_er else 'N/A'
        ai_time = ai_er.execution_time_ms if ai_er else 'N/A'
        ai_pass_rate = f"{ai_er.pass_rate:.2f}%" if ai_er else 'N/A'
        ai_passed = ai_er.passed_count if ai_er else 'N/A'
        ai_failed = ai_er.failed_count if ai_er else 'N/A'
        ai_errors = ai_er.error_count if ai_er else 'N/A'
        ai_timeouts = ai_er.timeout_count if ai_er else 'N/A'
        hu_status = hu_er.execution_status if hu_er else 'N/A'
        hu_time = hu_er.execution_time_ms if hu_er else 'N/A'
        hu_pass_rate = f"{hu_er.pass_rate:.2f}%" if hu_er else 'N/A'
        hu_passed = hu_er.passed_count if hu_er else 'N/A'
        hu_failed = hu_er.failed_count if hu_er else 'N/A'
        hu_errors = hu_er.error_count if hu_er else 'N/A'
        hu_timeouts = hu_er.timeout_count if hu_er else 'N/A'

        tool_unavail_ai = next((f.message for f in ai_static if f.rule == 'TOOL_UNAVAILABLE'), 'available') or 'available'
        tool_unavail_hu = next((f.message for f in hu_static if f.rule == 'TOOL_UNAVAILABLE'), 'available') or 'available'

        # Security tool status: look for bandit (Python) or spotbugs (Java) notes specifically
        def _security_tool_status(static_findings):
            for f in static_findings:
                msg = (f.message or '').lower()
                if f.rule == 'TOOL_UNAVAILABLE' and ('bandit' in msg or 'spotbugs' in msg):
                    return f.message
            # Check for positive completion note
            for f in static_findings:
                msg = (f.message or '').lower()
                if 'spotbugs' in msg and 'analysis completed' in msg:
                    return f.message
                if 'bandit' in msg and ('analysis completed' in msg or 'finding' in msg):
                    return f.message
            return 'Analysis completed — tool ran successfully.'

        def _quality_tool_status(static_findings):
            for f in static_findings:
                msg = (f.message or '').lower()
                if f.rule == 'TOOL_UNAVAILABLE' and ('ruff' in msg or 'pmd' in msg):
                    return f.message
            for f in static_findings:
                msg = (f.message or '').lower()
                if ('ruff' in msg or 'pmd' in msg) and 'analysis completed' in msg:
                    return f.message
            return 'Analysis completed — tool ran successfully.'

        security_tool_status_ai = _security_tool_status(ai_static)
        security_tool_status_hu = _security_tool_status(hu_static)
        tool_unavail_quality_ai = _quality_tool_status(ai_static)
        tool_unavail_quality_hu = _quality_tool_status(hu_static)

        # Dataset classification derived from the authoritative is_pilot field
        data_classification = "PILOT / TEST DATA" if comparison.is_pilot else "RESEARCH DATA"
        data_classification_note = (
            "This comparison is classified as PILOT / TEST DATA and should not be used as primary research evidence."
            if comparison.is_pilot
            else "This comparison is classified as RESEARCH DATA and is included in the research dataset."
        )

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=18, spaceAfter=12, alignment=1)
    heading1 = ParagraphStyle('H1Custom', parent=styles['Heading1'], fontSize=14, spaceAfter=8, spaceBefore=14, textColor=colors.HexColor('#1e3a8a'))
    heading2 = ParagraphStyle('H2Custom', parent=styles['Heading2'], fontSize=12, spaceAfter=6, spaceBefore=10, textColor=colors.HexColor('#0f172a'))
    body = ParagraphStyle('BodyCustom', parent=styles['BodyText'], fontSize=10, leading=14, spaceAfter=6)
    mono = ParagraphStyle('MonoCustom', parent=styles['Code'], fontSize=9, leading=12, spaceAfter=6)
    caption = ParagraphStyle('CaptionCustom', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=1, spaceAfter=12)

    story.append(Paragraph("Research Code Evaluator — Detailed Report", title_style))
    story.append(Paragraph(
        "An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development",
        ParagraphStyle('AimStyle', parent=styles['Normal'], fontSize=11,
                       alignment=1, textColor=colors.HexColor('#1e3a8a'),
                       spaceAfter=6, spaceBefore=2, leading=16)
    ))
    story.append(Paragraph(
        f"Problem: <b>{title}</b> &nbsp;·&nbsp; Category: <b>{category}</b> &nbsp;·&nbsp; Difficulty: <b>{difficulty}</b>",
        ParagraphStyle('ProblemLine', parent=styles['Normal'], fontSize=12,
                       alignment=1, textColor=colors.HexColor('#0f172a'),
                       spaceAfter=4, spaceBefore=2, leading=16)
    ))
    story.append(Paragraph(f"Comparison #{comparison_id} · Generated {_utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", caption))
    story.append(Spacer(1, 8))

    def h1(text):
        story.append(Paragraph(text, heading1))
    def h2(text):
        story.append(Paragraph(text, heading2))
    def p(text):
        story.append(Paragraph(text, body))
    def code(text):
        story.append(Paragraph(f"<code>{_esc(text)}</code>", mono))
    def table_row(*cells):
        return [Paragraph(str(c) if c is not None else 'N/A', body) for c in cells]

    # ── OVERALL RESULT SUMMARY BLOCK (at the very top) ────────────────────
    overall_dir = next((r.direction for r in comp_rows if r.metric == "overall"), "N/A")
    winner_color = {
        "AI": colors.HexColor("#dbeafe"),
        "HUMAN": colors.HexColor("#ccfbf1"),
        "COMPARABLE": colors.HexColor("#f1f5f9"),
    }.get(overall_dir, colors.HexColor("#f1f5f9"))
    winner_label = {
        "AI": f"AI ({ai_name}) scored higher",
        "HUMAN": "Human scored higher",
        "COMPARABLE": "Comparable — no clear winner",
    }.get(overall_dir, "N/A")

    summary_style = ParagraphStyle('SummaryBox', parent=styles['Normal'], fontSize=11,
                                   leading=16, spaceAfter=6, spaceBefore=4,
                                   backColor=winner_color, borderPadding=(8, 10, 8, 10))

    summary_data = [
        ["OVERALL RESULT", ""],
        [f"AI Overall Score", f"{ai_overall:.3f} / 100" if ai_overall is not None else "N/A"],
        [f"Human Overall Score", f"{hu_overall:.3f} / 100" if hu_overall is not None else "N/A"],
        ["Difference (AI − Human)", f"{round(ai_overall - hu_overall, 3):.3f}" if ai_overall is not None and hu_overall is not None else "N/A"],
        ["Result", winner_label],
        ["Data Classification", data_classification],
    ]
    # Dimension outcomes
    dims_short = ["reliability", "performance", "maintainability", "security", "complexity", "code_quality"]
    for metric_name in dims_short:
        r = next((r for r in comp_rows if r.metric == metric_name), None)
        if r:
            summary_data.append([f"  {metric_name.replace('_', ' ').title()}", r.direction])

    summary_table = Table(summary_data, colWidths=[260, 220])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), winner_color),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 4), (-1, 4), [colors.HexColor('#fef9c3')]),  # highlight winner row
    ]))
    story.append(summary_table)
    story.append(Paragraph(
        "This result applies only to this single comparison. It does not establish universal superiority of AI or human code.",
        ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=8,
                       textColor=colors.grey, spaceAfter=12, spaceBefore=4)
    ))
    story.append(Spacer(1, 6))

    # Header
    h1("1. Report Header")
    header_data = [
        table_row("Comparison ID", comparison_id),
        table_row("Problem", title),
        table_row("Category", category),
        table_row("Difficulty", difficulty),
        table_row("Language", comparison.language),
        table_row("AI System", ai_name),
        table_row("Experiment Type", comparison.experiment_type),
        table_row("Data Classification", data_classification),
        table_row("Status", status),
        table_row("Problem Version", problem_version),
        table_row("Test Case Version", test_case_version),
        table_row("Created", created),
        table_row("Completed", completed),
        table_row("Timeout", f"{timeout} seconds"),
    ]
    header_table = Table([[c] for r in header_data for c in r], colWidths=[180, 300])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    h1("2. Research Objective")
    p(f"This report presents the results of a controlled comparison between AI-generated code and human-written code for the problem \"{title}\". The evaluation measures reliability, performance, maintainability, security, complexity, and code quality using identical test cases and analysis tools.")

    h1("3. Dataset Classification")
    p(f"<b>{data_classification}</b> — {data_classification_note}")

    h1("4. Problem Definition")
    p(desc)

    h1("5. Test Cases")
    if problem:
        test_cases = session.query(models.TestCase).filter_by(problem_id=problem.problem_id).all()
        tc_data = [["#", "Input", "Expected Output"]] + [[tc.test_case_id, _esc(tc.input), _esc(tc.expected_output)] for tc in test_cases]
        tc_table = Table(tc_data, colWidths=[40, 240, 200])
        tc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(tc_table)
    story.append(Spacer(1, 8))

    h1("6. AI Code")
    code(comparison.ai_source_code)

    h1("7. Human Code")
    code(comparison.human_source_code)

    h1("8. Execution Results")
    h2("AI Execution")
    exec_data = [
        ["Status", ai_status], ["Time (ms)", ai_time], ["Pass Rate", ai_pass_rate],
        ["Passed", ai_passed], ["Failed", ai_failed], ["Errors", ai_errors], ["Timeouts", ai_timeouts]
    ]
    exec_table = Table(exec_data, colWidths=[120, 320])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 6))

    h2("Human Execution")
    exec_data = [
        ["Status", hu_status], ["Time (ms)", hu_time], ["Pass Rate", hu_pass_rate],
        ["Passed", hu_passed], ["Failed", hu_failed], ["Errors", hu_errors], ["Timeouts", hu_timeouts]
    ]
    exec_table = Table(exec_data, colWidths=[120, 320])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 8))

    h1("9. Reliability")
    p("<b>Formula:</b> Pass Rate = (Passed Test Cases / Total Test Cases) × 100")
    rel_data = [
        ["Variant", "Total", "Passed", "Failed", "Errors", "Timeouts", "Pass Rate"],
        ["AI", ai_er.total_test_cases if ai_er else 'N/A', ai_passed, ai_failed, ai_errors, ai_timeouts, ai_pass_rate],
        ["Human", hu_er.total_test_cases if hu_er else 'N/A', hu_passed, hu_failed, hu_errors, hu_timeouts, hu_pass_rate],
    ]
    rel_table = Table(rel_data, colWidths=[70, 70, 70, 70, 70, 70, 100])
    rel_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(rel_table)
    story.append(Spacer(1, 8))

    h1("10. Performance")
    p("Lower execution time represents better observed performance.")
    perf_data = [
        ["Variant", "Execution Time (ms)", "Status"],
        ["AI", ai_time, ai_status],
        ["Human", hu_time, hu_status],
    ]
    perf_table = Table(perf_data, colWidths=[150, 180, 150])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 8))

    h1("11. Maintainability")
    p("<b>Formula:</b> 0.30 × Cyclomatic Component + 0.20 × Function Length Component + 0.20 × Nesting Component + 0.30 × Coupling Component")
    maint_data = [
        ["Variant", "Cyclomatic", "Function Length", "Nesting", "Coupling", "Final Score"],
        ["AI", ai_complexity.get('cyclomatic_avg', 'N/A'), ai_complexity.get('function_length_avg', 'N/A'),
         ai_complexity.get('nesting_depth_avg', 'N/A'), ai_complexity.get('coupling', 'N/A'),
         ai_dim['maintainability'].dimension_score if ai_dim.get('maintainability') else 'N/A'],
        ["Human", hu_complexity.get('cyclomatic_avg', 'N/A'), hu_complexity.get('function_length_avg', 'N/A'),
         hu_complexity.get('nesting_depth_avg', 'N/A'), hu_complexity.get('coupling', 'N/A'),
         hu_dim['maintainability'].dimension_score if hu_dim.get('maintainability') else 'N/A'],
    ]
    maint_table = Table(maint_data, colWidths=[60, 100, 110, 80, 80, 80])
    maint_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(maint_table)
    story.append(Spacer(1, 8))

    h1("12. Security")
    p("Fewer security findings represent better observed security posture.")
    p(f"<b>Security tool (Python):</b> Bandit &nbsp;|&nbsp; <b>Security tool (Java):</b> SpotBugs")
    sec_data = [
        ["Variant", "Tool", "Findings Count", "Tool Status"],
        ["AI", "Bandit (Python) / SpotBugs (Java)", len(ai_sec), security_tool_status_ai],
        ["Human", "Bandit (Python) / SpotBugs (Java)", len(hu_sec), security_tool_status_hu],
    ]
    sec_table = Table(sec_data, colWidths=[70, 150, 90, 170])
    sec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(sec_table)
    story.append(Spacer(1, 8))

    h1("13. Complexity")
    p("Lower complexity represents better observed maintainability.")
    comp_data = [
        ["Metric", "AI Raw", "Human Raw"],
        ["Cyclomatic Avg", ai_complexity.get('cyclomatic_avg', 'N/A'), hu_complexity.get('cyclomatic_avg', 'N/A')],
        ["Function Length Avg", ai_complexity.get('function_length_avg', 'N/A'), hu_complexity.get('function_length_avg', 'N/A')],
        ["Nesting Depth Avg", ai_complexity.get('nesting_depth_avg', 'N/A'), hu_complexity.get('nesting_depth_avg', 'N/A')],
        ["Coupling", ai_complexity.get('coupling', 'N/A'), hu_complexity.get('coupling', 'N/A')],
    ]
    comp_table = Table(comp_data, colWidths=[200, 160, 160])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 8))

    h1("14. Code Quality")
    p("Fewer code-quality findings represent better observed code quality.")
    p(f"<b>Code quality tool (Python):</b> Ruff &nbsp;|&nbsp; <b>Code quality tool (Java):</b> PMD")
    quality_data = [
        ["Variant", "Tool", "Findings Count", "Tool Status"],
        ["AI", "Ruff (Python) / PMD (Java)", len(ai_quality), tool_unavail_quality_ai],
        ["Human", "Ruff (Python) / PMD (Java)", len(hu_quality), tool_unavail_quality_hu],
    ]
    quality_table = Table(quality_data, colWidths=[70, 150, 90, 170])
    quality_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(quality_table)
    story.append(Spacer(1, 8))

    h1("15. Score Calculation")
    p("<b>Formula:</b> Overall Score = Σ (Normalized Dimension Score × Dimension Weight)")
    score_rows = [["Dimension", "AI Raw", "AI Norm", "Weight", "AI Contrib", "Human Raw", "Human Norm", "Human Contrib"]]
    for d in dims:
        ai_s = ai_dim[d]
        hu_s = hu_dim[d]
        w = weights.get(d, 0)
        ai_norm = ai_s.normalized_value if ai_s else None
        hu_norm = hu_s.normalized_value if hu_s else None
        ai_contrib = f"{round((ai_norm or 0) * w, 3):.3f}" if ai_norm is not None else 'N/A'
        hu_contrib = f"{round((hu_norm or 0) * w, 3):.3f}" if hu_norm is not None else 'N/A'
        score_rows.append([
            d,
            f"{ai_s.raw_value:.3f}" if ai_s and ai_s.raw_value is not None else 'N/A',
            f"{ai_norm:.3f}" if ai_norm is not None else 'N/A',
            f"{w:.2f}",
            ai_contrib,
            f"{hu_s.raw_value:.3f}" if hu_s and hu_s.raw_value is not None else 'N/A',
            f"{hu_norm:.3f}" if hu_norm is not None else 'N/A',
            hu_contrib,
        ])
    score_rows.append([
        "Overall", "", "", "",
        f"{ai_overall:.3f}" if ai_overall is not None else 'N/A',
        "", "", f"{hu_overall:.3f}" if hu_overall is not None else 'N/A',
    ])
    score_table = Table(score_rows, colWidths=[70, 60, 60, 55, 65, 60, 60, 65])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8fafc')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 8))

    h1("16. Normalization Details")
    p(f"<b>Methodology:</b> Dataset min/max normalization")
    p(f"<b>Higher-is-Better Formula:</b> (x - min) / (max - min) × 100")
    p(f"<b>Lower-is-Better Formula:</b> (max - x) / (max - min) × 100")
    p(f"<b>Neutral Value:</b> {neutral}")

    h1("17. AI vs Human Comparison")
    comp_data = [["Metric", "AI", "Human", "Difference", "Direction"]] + [
        [_esc(r.metric), r.ai_value if r.ai_value is not None else 'N/A', r.human_value if r.human_value is not None else 'N/A',
         r.difference if r.difference is not None else 'N/A', _esc(r.direction)] for r in comp_rows
    ]
    comp_table = Table(comp_data, colWidths=[100, 80, 80, 80, 120])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 1), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 8))

    h1("18. Statistical Analysis")
    p(f"<b>Alpha:</b> {alpha}")
    p("<b>Test:</b> Wilcoxon Signed-Rank")
    if stats.get("has_sufficient_data"):
        stat_data = [["Metric", "N Paired", "Statistic", "P-Value", "Significant", "Effect Size", "Status"]]
        for metric, data in stats.get("per_metric", {}).items():
            stat_data.append([
                _esc(metric), data.get('n_paired', 'N/A'), data.get('statistic', 'N/A'),
                data.get('p_value', 'N/A'), 'Yes' if data.get('significant') else 'No',
                data.get('effect_size', 'N/A'), _esc(data.get('status', 'N/A'))
            ])
        stat_table = Table(stat_data, colWidths=[80, 60, 70, 70, 70, 70, 100])
        stat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 1), (5, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(stat_table)
    else:
        p("<i>Insufficient data for statistical analysis. Statistical analysis requires multiple paired comparisons.</i>")
    story.append(Spacer(1, 8))

    h1("19. Interpretation")
    p("This result applies only to this comparison and does not establish a universal superiority of AI-generated code.")

    h1("20. Limitations / Threats to Validity")
    story.append(Paragraph("• Single comparison — does not establish universal superiority.", body))
    story.append(Paragraph("• Pilot/test data — results may not be representative of broader populations.", body))
    story.append(Paragraph("• Tool availability — security and code-quality scores depend on installed analysis tools.", body))
    story.append(Paragraph("• Dynamic normalization — scores are relative to the accumulated dataset at the time of scoring.", body))

    h1("21. Reproducibility")
    p("To reproduce this comparison, use the same problem, test cases, AI code, human code, language, execution timeout, and scoring configuration. Store the database file and export artifacts together.")

    h1("22. Source Code Appendix")
    h2("AI Source Code")
    code(comparison.ai_source_code)
    h2("Human Source Code")
    code(comparison.human_source_code)

    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Research Code Evaluator · An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development · Report generated {_utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", caption))

    doc.build(story)
    return buf.getvalue()
