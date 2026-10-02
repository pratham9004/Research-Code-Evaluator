import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import DetailedReport from '../pages/DetailedReport';

const { getDetailedComparison } = vi.hoisted(() => ({ getDetailedComparison: vi.fn() }));
vi.mock('../api', () => ({ api: { getDetailedComparison, exportResearchReportPdf: vi.fn() } }));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('raw execution detailed report', () => {
  it('renders results when comparison scores and maintainability are absent', async () => {
    const oneCase = {
      test_case_id: 500, input: '{"requested":"read"}', status: 'FAIL',
      actual_output: 'denied', expected_output: 'granted', error: null,
      execution_time_ms: 0.2, exit_code: 0, stdout: '', stderr: '',
    };
    getDetailedComparison.mockResolvedValue({
      experiment: {
        comparison_id: 50, problem_id: 'P050', problem_title: 'Access Scope Validator',
        category: 'security', difficulty: 'medium', language: 'python', ai_name: 'ChatGPT',
        status: 'execution_only', created_at: '', completed_at: '', execution_timeout_seconds: 10,
        test_case_count: 1, ai_code_available: true, human_code_available: true,
        experiment_type: 'RESEARCH', is_pilot: false, problem_version: 1, test_case_version: 1,
        data_classification: 'RESEARCH DATA',
      },
      executive_result: { ai_overall: null, human_overall: null, difference: null,
        percentage_difference: null, direction: null, neutral_statement: '' },
      preflight: { ai: [], human: [] }, six_dimensions: [],
      reliability: {
        formula: 'Observed pass rate',
        ai: { execution_status: 'FAIL', execution_time_ms: 0.2, pass_rate: 0, total_test_cases: 1,
          passed_count: 0, failed_count: 1, error_count: 0, timeout_count: 0,
          cases: [oneCase] },
        human: { execution_status: 'PASS', execution_time_ms: 0.1, pass_rate: 100, total_test_cases: 1,
          passed_count: 1, failed_count: 0, error_count: 0, timeout_count: 0,
          cases: [{ ...oneCase, status: 'PASS', actual_output: 'granted', execution_time_ms: 0.1 }] },
      },
      performance: { ai: { execution_time_ms: 0.2, execution_status: 'FAIL', normalized_value: null },
        human: { execution_time_ms: 0.1, execution_status: 'PASS', normalized_value: null },
        note: 'Measured execution time.' },
      test_cases: { ai: [oneCase], human: [{ ...oneCase, status: 'PASS' }] },
      interpretation: { statement: '', disclaimer: '' },
    } as any);

    render(<DetailedReport reportId={50} onBack={() => {}} />);
    expect(await screen.findByText('Detailed Raw Execution Report #50')).toBeTruthy();
    expect(screen.getAllByText('{"requested":"read"}')).toHaveLength(2);
    expect(screen.getByText('denied')).toBeTruthy();
    expect(screen.getAllByText('granted').length).toBeGreaterThan(0);
    expect(screen.getByText(/comparative scores and an AI\/Human winner have not been calculated/i)).toBeTruthy();
    expect(screen.queryByText('Overall comparison:')).toBeNull();
  });
});
