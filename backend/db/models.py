from __future__ import annotations

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Problem(Base):
    __tablename__ = "problems"

    problem_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    supported_languages = Column(JSON, nullable=False)
    version = Column(Integer, default=1)
    input_spec = Column(Text, nullable=True)
    output_spec = Column(Text, nullable=True)
    constraints = Column(Text, nullable=True)
    starter_template = Column(Text, nullable=True)
    active = Column(Integer, nullable=False, default=1)
    signature_python = Column(String, nullable=True)
    signature_java = Column(String, nullable=True)
    signature_cpp = Column(String, nullable=True)
    signature_javascript = Column(String, nullable=True)
    entry_function = Column(String, nullable=False, default="solve")
    research_focus = Column(String, nullable=True)
    security_relevance = Column(String, nullable=True)  # low / medium / high
    harness_type = Column(String, nullable=False, default="legacy")  # "legacy" | "typed"
    # Per-language starter templates (shown in editor as the function skeleton)
    starter_template_python = Column(Text, nullable=True)
    starter_template_java = Column(Text, nullable=True)
    starter_template_cpp = Column(Text, nullable=True)
    starter_template_javascript = Column(Text, nullable=True)

    test_cases = relationship(
        "TestCase", back_populates="problem", cascade="all, delete-orphan"
    )


class TestCase(Base):
    __tablename__ = "test_cases"

    test_case_id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(String, ForeignKey("problems.problem_id"), nullable=False)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    case_type = Column(String, default="functional")
    version = Column(Integer, default=1)

    problem = relationship("Problem", back_populates="test_cases")


class Comparison(Base):
    __tablename__ = "comparisons"

    comparison_id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(String, ForeignKey("problems.problem_id"), nullable=False)
    language = Column(String, nullable=False)
    ai_name = Column(String, nullable=False)
    ai_source_code = Column(Text, nullable=False)
    human_source_code = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=_utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_pilot = Column(Integer, nullable=False, default=1)
    experiment_type = Column(String, nullable=False, default="PILOT")
    problem_version = Column(Integer, nullable=True)
    test_case_version = Column(Integer, nullable=True)


class ExecutionResult(Base):
    __tablename__ = "execution_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)  # AI or HUMAN
    total_test_cases = Column(Integer, nullable=False)
    passed_count = Column(Integer, nullable=False)
    failed_count = Column(Integer, nullable=False)
    error_count = Column(Integer, nullable=False)
    timeout_count = Column(Integer, nullable=False)
    pass_rate = Column(Float, nullable=True)
    execution_time_ms = Column(Float, nullable=True)
    execution_status = Column(String, nullable=False)  # PASS / FAIL / ERROR / TIMEOUT
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)


class PreflightResult(Base):
    __tablename__ = "preflight_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)
    status = Column(String, nullable=False)  # PASS / FAIL
    message = Column(Text, nullable=True)
    checked_at = Column(DateTime, default=_utcnow)


class TestCaseResult(Base):
    __tablename__ = "test_case_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)
    test_case_id = Column(Integer, ForeignKey("test_cases.test_case_id"), nullable=False)
    status = Column(String, nullable=False)  # PASS / FAIL / ERROR / TIMEOUT
    actual_output = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    execution_time_ms = Column(Float, nullable=True)
    exit_code = Column(Integer, nullable=True)
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=_utcnow)


class StaticAnalysisResult(Base):
    __tablename__ = "static_analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)
    tool_name = Column(String, nullable=False)
    tool_version = Column(String, nullable=True)
    rule = Column(String, nullable=True)
    category = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    source_location = Column(String, nullable=True)
    raw_result = Column(Text, nullable=True)


class ComplexityData(Base):
    __tablename__ = "complexity_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)
    metric_name = Column(String, nullable=False)
    raw_value = Column(Float, nullable=False)


class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)
    tool = Column(String, nullable=True)
    tool_version = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    rule = Column(String, nullable=True)
    category = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    location = Column(String, nullable=True)


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    code_variant = Column(String, nullable=False)
    dimension = Column(String, nullable=False)
    raw_value = Column(Float, nullable=True)
    normalized_value = Column(Float, nullable=True)
    weighted_value = Column(Float, nullable=True)
    dimension_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    scoring_config_version = Column(Integer, default=1)
    normalization_population_min = Column(Float, nullable=True)
    normalization_population_max = Column(Float, nullable=True)
    normalization_population_n = Column(Integer, nullable=True)


class ComparisonResult(Base):
    __tablename__ = "comparison_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    metric = Column(String, nullable=False)
    ai_value = Column(Float, nullable=True)
    human_value = Column(Float, nullable=True)
    difference = Column(Float, nullable=True)
    direction = Column(String, nullable=True)
    percentage_difference = Column(Float, nullable=True)
    statistical_status = Column(String, nullable=True)


class StatisticalResult(Base):
    __tablename__ = "statistical_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.comparison_id"), nullable=False)
    metric = Column(String, nullable=False)
    test = Column(String, nullable=False, default="wilcoxon_signed_rank")
    n_paired = Column(Integer, nullable=True)
    statistic = Column(Float, nullable=True)
    p_value = Column(Float, nullable=True)
    significant = Column(Integer, nullable=True)
    effect_size = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="insufficient_data")
    alpha = Column(Float, nullable=True)
    dataset_used = Column(String, nullable=True)
    computed_at = Column(DateTime, default=_utcnow)
