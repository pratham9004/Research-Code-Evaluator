export interface TestCase {
  test_case_id: number;
  input: string;
  expected_output: string;
  case_type: string;
}

export interface Problem {
  problem_id: string;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  supported_languages: string[];
  signature_python?: string;
  signature_java?: string;
  signature_cpp?: string;
  signature_javascript?: string;
  entry_function: string;
  compared: boolean;
  test_case_count: number;
  test_cases?: TestCase[];
  input_spec?: string;
  output_spec?: string;
  constraints?: string;
  starter_template?: string;
  active?: boolean;
  version?: number;
  research_focus?: string;
  security_relevance?: string;
  harness_type?: string;
  starter_template_python?: string;
  starter_template_java?: string;
  starter_template_cpp?: string;
  starter_template_javascript?: string;
}

export interface ComparisonSummary {
  comparison_id: number;
  problem_id: string;
  problem_title: string;
  language: string;
  ai_name: string;
  status: string;
  experiment_type: string;
  is_pilot: boolean;
  created_at: string;
  overall_winner: string | null;
  ai_overall: number | null;
  human_overall: number | null;
}

export interface DashboardData {
  has_data: boolean;
  kpis: {
    total_problems: number;
    problems_compared: number;
    problems_remaining: number;
    completion_percentage: number;
    total_comparisons: number;
    raw_execution_datasets: number;
    incomplete_comparisons: number;
    pilot_comparisons: number;
    ai_systems_count: number;
  };
  ai_systems: Record<string, number>;
  outcomes: { ai_better: number; human_better: number; comparable: number };
  metric_averages: Record<string, { label: string; ai: number | null; human: number | null }>;
  recent_comparisons: Array<{
    comparison_id: number;
    problem_title: string;
    language: string;
    ai_name: string;
    created_at: string | null;
    overall_winner: string;
    ai_overall: number | null;
    human_overall: number | null;
  }>;
  python_benchmark_results?: Array<{
    problem_id: string;
    problem_name: string;
    comparison_id: number | null;
    ai: PythonBenchmarkVariant;
    human: PythonBenchmarkVariant;
  }>;
}

export interface PythonBenchmarkVariant {
  status: string;
  total: number;
  passed: number;
  failed: number;
  errors: number;
  timeouts: number;
  execution_time_ms: number | null;
  error_message: string | null;
}

export interface ComparisonMetric {
  metric: string;
  ai_value: number;
  human_value: number;
  difference: number | null;
  direction: string | null;
  percentage_difference: number | null;
  statistical_status: string;
}

export interface MaintainabilityComponent {
  raw_value: number;
  reference_min: number;
  reference_max: number;
  normalized_score: number;
  weight: number;
  weighted_contribution: number;
}

export interface SecurityFinding {
  tool: string;
  tool_version: string;
  severity: string;
  rule: string;
  category: string;
  message: string;
  location: string;
}

export interface StaticAnalysisFinding {
  tool_name: string;
  tool_version: string;
  rule: string;
  category: string;
  severity: string;
  message: string;
  source_location: string;
  raw_result: string;
}

export interface TestCaseResult {
  test_case_id: number;
  input?: string | null;
  status: string;
  actual_output: string | null;
  expected_output: string | null;
  error: string | null;
  execution_time_ms: number | null;
  exit_code: number | null;
  stdout: string | null;
  stderr: string | null;
  recorded_at?: string;
}

export interface ExecutionSummary {
  execution_status: string;
  execution_time_ms: number | null;
  pass_rate: number | null;
  total_test_cases: number;
  passed_count: number;
  failed_count: number;
  error_count: number;
  timeout_count: number;
  cases?: TestCaseResult[];
}

export interface ScoreDimension {
  dimension: string;
  raw_value: number | null;
  normalized_value: number | null;
  normalization_population_min: number | null;
  normalization_population_max: number | null;
  normalization_population_n: number | null;
  weighted_value: number | null;
  dimension_score: number | null;
}

export interface Report {
  comparison_id: number;
  problem_id: string;
  problem_title: string;
  language: string;
  ai_name: string;
  status: string;
  experiment_type: string;
  is_pilot: boolean;
  problem_version: number | null;
  test_case_version: number | null;
  created_at: string;
  completed_at: string;
  data_classification: string;
  execution: {
    ai: ExecutionSummary;
    human: ExecutionSummary;
  };
  preflight: {
    ai: Array<{ status: string; message: string }>;
    human: Array<{ status: string; message: string }>;
  };
  scores: {
    ai: ScoreDimension[];
    human: ScoreDimension[];
    ai_overall: number | null;
    human_overall: number | null;
  };
  comparison: ComparisonMetric[];
}

export interface DetailedReport {
  experiment: {
    comparison_id: number;
    problem_id: string;
    problem_title: string | null;
    category: string | null;
    difficulty: string | null;
    language: string;
    ai_name: string;
    status: string;
    experiment_type: string;
    is_pilot: boolean;
    problem_version: number | null;
    test_case_version: number | null;
    created_at: string | null;
    completed_at: string | null;
    execution_timeout_seconds: number;
    test_case_count: number;
    ai_code_available: boolean;
    human_code_available: boolean;
    data_classification: string;
  };
  executive_result: {
    ai_overall: number | null;
    human_overall: number | null;
    difference: number | null;
    percentage_difference: number | null;
    direction: string | null;
    neutral_statement: string;
  };
  six_dimensions: Array<{
    dimension: string;
    ai_value: number | null;
    human_value: number | null;
    difference: number | null;
    direction: string | null;
    percentage_difference: number | null;
  }>;
  preflight: {
    ai: Array<{ status: string; message: string }>;
    human: Array<{ status: string; message: string }>;
  };
  reliability: {
    ai: ExecutionSummary & { cases: TestCaseResult[] };
    human: ExecutionSummary & { cases: TestCaseResult[] };
    formula: string;
  };
  performance: {
    ai: { execution_time_ms: number | null; execution_status: string | null; normalized_value: number | null };
    human: { execution_time_ms: number | null; execution_status: string | null; normalized_value: number | null };
    direction: string;
    note: string;
  };
  maintainability: {
    ai: { components: Record<string, MaintainabilityComponent>; final_score: number | null };
    human: { components: Record<string, MaintainabilityComponent>; final_score: number | null };
    formula: string;
    reference_bounds: Record<string, { min: number; max: number }>;
    weights: Record<string, number>;
  };
  security: {
    ai: { findings: SecurityFinding[]; count: number; tool_status: string | null };
    human: { findings: SecurityFinding[]; count: number; tool_status: string | null };
    direction: string | null;
    note: string;
  };
  complexity: {
    ai: Record<string, number>;
    human: Record<string, number>;
    normalized_ai: number | null;
    normalized_human: number | null;
    direction: string | null;
    note: string;
  };
  code_quality: {
    ai: { findings: StaticAnalysisFinding[]; count: number; tool_status: string | null };
    human: { findings: StaticAnalysisFinding[]; count: number; tool_status: string | null };
    normalized_ai: number | null;
    normalized_human: number | null;
    direction: string | null;
    note: string;
  };
  scoring_calculation: {
    weights: Record<string, number>;
    ai: {
      dimensions: Array<{
        dimension: string;
        raw_value: number | null;
        normalized_value: number | null;
        normalization_population_min: number | null;
        normalization_population_max: number | null;
        normalization_population_n: number | null;
        weight: number | null;
        weighted_contribution: number | null;
      }>;
      overall_score: number | null;
    };
    human: {
      dimensions: Array<{
        dimension: string;
        raw_value: number | null;
        normalized_value: number | null;
        normalization_population_min: number | null;
        normalization_population_max: number | null;
        normalization_population_n: number | null;
        weight: number | null;
        weighted_contribution: number | null;
      }>;
      overall_score: number | null;
    };
    formula: string;
  };
  normalization: {
    methodology: string;
    neutral_value: number;
    higher_is_better_formula: string;
    lower_is_better_formula: string;
    note: string;
  };
  ai_vs_human: Array<{
    metric: string;
    ai_value: number | null;
    human_value: number | null;
    difference: number | null;
    percentage_difference: number | null;
    direction: string;
    statistical_status: string;
  }>;
  statistical_analysis: {
    alpha: number | null;
    per_metric: Record<string, any>;
    has_sufficient_data: boolean;
  };
  test_cases: {
    ai: TestCaseResult[];
    human: TestCaseResult[];
  };
  raw_analysis: {
    ai_security_findings: SecurityFinding[];
    human_security_findings: SecurityFinding[];
    ai_static_analysis: StaticAnalysisFinding[];
    human_static_analysis: StaticAnalysisFinding[];
    ai_complexity: Record<string, number>;
    human_complexity: Record<string, number>;
  };
  interpretation: {
    statement: string;
    disclaimer: string;
  };
}
