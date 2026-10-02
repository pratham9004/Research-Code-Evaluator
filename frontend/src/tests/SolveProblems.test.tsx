import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import SolveProblems from '../pages/SolveProblems';

const problems = [
  {
    problem_id: 'P001',
    title: 'Two Sum',
    description: 'desc',
    category: 'Algorithms',
    difficulty: 'Easy',
    supported_languages: ['python'],
    signature_python: 'def solve(d):',
    signature_java: '',
    entry_function: 'solve',
    compared: false,
    test_case_count: 5,
    research_focus: 'Correctness, algorithmic approach',
    security_relevance: 'low',
  },
];

vi.mock('../api', () => ({
  api: {
    getProblems: () => Promise.resolve(problems),
    submitComparison: () => Promise.resolve({ comparison_id: 1 }),
  },
}));

describe('Solve Problems smoke test', () => {
  it('validates code inputs before submitting', async () => {
    render(<SolveProblems onReport={() => {}} />);
    await screen.findByRole('option', { name: /P001.*Two Sum.*Reliability/i });
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'P001' } });
    fireEvent.click(await screen.findByText('Submit & Compare'));
    expect(await screen.findByText('Both AI and Human code are required.')).toBeTruthy();
  });
});
