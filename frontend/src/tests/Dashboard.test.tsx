import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import Dashboard from '../pages/Dashboard';

const { getDashboard } = vi.hoisted(() => ({ getDashboard: vi.fn() }));
vi.mock('../api', () => ({ api: { getDashboard } }));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('Python benchmark dashboard results', () => {
  it('does not show benchmark problem definitions as missing executions', async () => {
    getDashboard.mockResolvedValue({
      has_data: false,
      kpis: { total_problems: 50, problems_compared: 0, problems_remaining: 50, completion_percentage: 0,
        total_comparisons: 0, incomplete_comparisons: 0, pilot_comparisons: 0, ai_systems_count: 0 },
      ai_systems: {}, outcomes: { ai_better: 0, human_better: 0, comparable: 0 },
      metric_averages: {}, recent_comparisons: [], python_benchmark_results: [],
    });

    render(<Dashboard />);
    expect(await screen.findByText('No valid paired comparison data available.')).toBeTruthy();
    expect(screen.queryByText('Python ChatGPT and Human Results (P001-P050)')).toBeNull();
  });

  it('renders the P001-P050 ChatGPT and Human execution rows', async () => {
    const rows = Array.from({ length: 50 }, (_, index) => {
      const id = `P${String(index + 1).padStart(3, '0')}`;
      const variant = {
        status: 'PASS', total: 10, passed: 10, failed: 0, errors: 0,
        timeouts: 0, execution_time_ms: 1.25, error_message: null,
      };
      return { problem_id: id, problem_name: `Problem ${id}`, comparison_id: index + 1, ai: variant, human: variant };
    });
    getDashboard.mockResolvedValue({
      has_data: false,
      kpis: { total_problems: 50, problems_compared: 0, problems_remaining: 50, completion_percentage: 0,
        total_comparisons: 0, incomplete_comparisons: 0, pilot_comparisons: 0, ai_systems_count: 0 },
      ai_systems: {}, outcomes: { ai_better: 0, human_better: 0, comparable: 0 },
      metric_averages: {}, recent_comparisons: [], python_benchmark_results: rows,
    });

    const { container } = render(<Dashboard />);
    expect(await screen.findByText('Python ChatGPT and Human Results (P001-P050)')).toBeTruthy();
    expect(screen.getByText('P001')).toBeTruthy();
    expect(screen.getByText('P050')).toBeTruthy();
    expect(container.querySelectorAll('tbody tr')).toHaveLength(50);
    expect(container.querySelector('tbody')?.textContent).toContain('10/10 pass, 0 fail, 0 errors, 0 timeouts');
  });
});
