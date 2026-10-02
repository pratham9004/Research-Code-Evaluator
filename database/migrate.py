"""Database migration script for schema updates.

Run: python -m database.migrate
"""
from __future__ import annotations

import sqlite3

from backend.config import DATABASE_PATH


def migrate():
    if not DATABASE_PATH.exists():
        print(f"Database not found at {DATABASE_PATH}")
        return

    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()

    # Add problem bank metadata columns
    for col, sql_type in (
        ("input_spec", "TEXT"),
        ("output_spec", "TEXT"),
        ("constraints", "TEXT"),
        ("starter_template", "TEXT"),
        ("active", "INTEGER"),
        ("signature_python", "TEXT"),
        ("signature_java", "TEXT"),
        ("signature_cpp", "TEXT"),
        ("signature_javascript", "TEXT"),
        ("research_focus", "TEXT"),
        ("security_relevance", "TEXT"),
    ):
        try:
            c.execute(f"ALTER TABLE problems ADD COLUMN {col} {sql_type}")
            print(f"Added problems.{col}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"problems.{col} already exists")
            else:
                print(f"Error adding problems.{col}: {e}")

    # Add experiment metadata columns to comparisons
    for col, sql in (
        ("experiment_type", "ALTER TABLE comparisons ADD COLUMN experiment_type VARCHAR NOT NULL DEFAULT 'PILOT'"),
        ("problem_version", "ALTER TABLE comparisons ADD COLUMN problem_version INTEGER"),
        ("test_case_version", "ALTER TABLE comparisons ADD COLUMN test_case_version INTEGER"),
    ):
        try:
            c.execute(sql)
            print(f"Added comparisons.{col}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"comparisons.{col} already exists")
            else:
                print(f"Error adding comparisons.{col}: {e}")

    # Add per-test-case timing and capture columns
    for col, sql in (
        ("execution_time_ms", "ALTER TABLE test_case_results ADD COLUMN execution_time_ms FLOAT"),
        ("exit_code", "ALTER TABLE test_case_results ADD COLUMN exit_code INTEGER"),
        ("stdout", "ALTER TABLE test_case_results ADD COLUMN stdout TEXT"),
        ("stderr", "ALTER TABLE test_case_results ADD COLUMN stderr TEXT"),
        ("recorded_at", "ALTER TABLE test_case_results ADD COLUMN recorded_at DATETIME"),
    ):
        try:
            c.execute(sql)
            print(f"Added test_case_results.{col}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"test_case_results.{col} already exists")
            else:
                print(f"Error adding test_case_results.{col}: {e}")

    # Add stdout/stderr/exit_code to execution_results
    for col, sql in (
        ("stdout", "ALTER TABLE execution_results ADD COLUMN stdout TEXT"),
        ("stderr", "ALTER TABLE execution_results ADD COLUMN stderr TEXT"),
        ("exit_code", "ALTER TABLE execution_results ADD COLUMN exit_code INTEGER"),
    ):
        try:
            c.execute(sql)
            print(f"Added execution_results.{col}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"execution_results.{col} already exists")
            else:
                print(f"Error adding execution_results.{col}: {e}")

    # Create preflight_results table
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS preflight_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comparison_id INTEGER NOT NULL,
                code_variant VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                message TEXT,
                checked_at DATETIME,
                FOREIGN KEY (comparison_id) REFERENCES comparisons(comparison_id)
            )
        """)
        print("Created preflight_results table")
    except sqlite3.OperationalError as e:
        print(f"Error creating preflight_results: {e}")

    # Missing executions must have NULL measurements, not fabricated zeroes.
    cols = {row[1]: row for row in c.execute("PRAGMA table_info(execution_results)")}
    if cols and (cols["pass_rate"][3] or cols["execution_time_ms"][3]):
        c.execute("""
            CREATE TABLE execution_results_nullable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comparison_id INTEGER NOT NULL,
                code_variant VARCHAR NOT NULL,
                total_test_cases INTEGER NOT NULL,
                passed_count INTEGER NOT NULL,
                failed_count INTEGER NOT NULL,
                error_count INTEGER NOT NULL,
                timeout_count INTEGER NOT NULL,
                pass_rate FLOAT,
                execution_time_ms FLOAT,
                execution_status VARCHAR NOT NULL,
                stdout TEXT,
                stderr TEXT,
                exit_code INTEGER,
                FOREIGN KEY (comparison_id) REFERENCES comparisons(comparison_id)
            )
        """)
        c.execute("""
            INSERT INTO execution_results_nullable
            SELECT id, comparison_id, code_variant, total_test_cases, passed_count,
                   failed_count, error_count, timeout_count,
                   CASE WHEN execution_status = 'MISSING' OR total_test_cases = 0 AND code_variant = 'HUMAN'
                        THEN NULL ELSE pass_rate END,
                   CASE WHEN execution_status = 'MISSING' OR total_test_cases = 0 AND code_variant = 'HUMAN'
                        THEN NULL ELSE execution_time_ms END,
                   execution_status, stdout, stderr, exit_code
            FROM execution_results
        """)
        c.execute("DROP TABLE execution_results")
        c.execute("ALTER TABLE execution_results_nullable RENAME TO execution_results")
        print("Made missing execution measurements nullable; preserved execution rows")

    # Normalize existing pilot records
    try:
        c.execute("UPDATE comparisons SET experiment_type = 'PILOT' WHERE is_pilot = 1")
        c.execute("UPDATE comparisons SET experiment_type = 'RESEARCH' WHERE is_pilot = 0")
        print("Normalized experiment_type for existing comparisons")
    except sqlite3.OperationalError as e:
        print(f"Error normalizing experiment_type: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()
