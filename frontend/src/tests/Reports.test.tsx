import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import Reports from '../pages/Reports';

const { listComparisons } = vi.hoisted(() => ({ listComparisons: vi.fn() }));
vi.mock('../api', () => ({ api: { listComparisons } }));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('raw execution dataset in Evaluations', () => {
  it('labels execution-only rows without a score or winner', async () => {
    listComparisons.mockResolvedValue([{
      comparison_id: 50, problem_id: 'P050', problem_title: 'Access Scope Validator',
      language: 'python', ai_name: 'ChatGPT', status: 'execution_only',
      experiment_type: 'RESEARCH', is_pilot: false, created_at: '',
      overall_winner: null, ai_overall: null, human_overall: null,
    }]);

    render(<Reports onOpen={() => {}} onOpenDetailed={() => {}} />);
    expect(await screen.findByText('RAW EXECUTION DATA')).toBeTruthy();
    expect(screen.getAllByText('Not calculated')).toHaveLength(3);
    expect(screen.queryByText('COMPLETED')).toBeNull();
  });
});
