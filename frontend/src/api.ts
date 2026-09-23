const BASE = '/api';

async function getJson(url: string) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${url} (${res.status})`);
  return res.json();
}

export const api = {
  getProblems: () => getJson(`${BASE}/problems`),
  getDashboard: () => getJson(`${BASE}/dashboard`),
  getStatistics: () => getJson(`${BASE}/statistics`),
  listComparisons: () => getJson(`${BASE}/comparisons`),
  getComparison: (id: number) => getJson(`${BASE}/comparisons/${id}`),
  getDetailedComparison: (id: number) => getJson(`${BASE}/comparisons/${id}/detailed`),
  submitComparison: async (payload: any) => {
    const res = await fetch(`${BASE}/comparisons`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const msg = await res.text();
      throw new Error(msg || `Submission failed (${res.status})`);
    }
    return res.json();
  },
  exportUrl: (format: 'csv' | 'json') => `${BASE}/export/dataset?format=${format}`,
  exportResearchReport: async () => {
    const res = await fetch(`${BASE}/export/research-report`);
    if (!res.ok) {
      const msg = await res.text();
      throw new Error(msg || `Export failed (${res.status})`);
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'research_report.xlsx';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  },
  exportResearchReportPdf: async (comparisonId: number) => {
    const res = await fetch(`${BASE}/export/research-report/pdf/${comparisonId}`);
    if (!res.ok) {
      const msg = await res.text();
      throw new Error(msg || `PDF export failed (${res.status})`);
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research_report_${comparisonId}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  },

  // ── Data Management ──────────────────────────────────────────────────
  getDataSummary: () => getJson(`${BASE}/data-management/summary`),

  previewDeleteByIds: async (ids: number[]) => {
    const res = await fetch(`${BASE}/data-management/preview/ids`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comparison_ids: ids }),
    });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },

  previewDeleteByDateRange: async (dateFrom: string, dateTo: string) => {
    const res = await fetch(`${BASE}/data-management/preview/date-range`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date_from: dateFrom, date_to: dateTo }),
    });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },

  previewDeleteAll: async () => {
    const res = await fetch(`${BASE}/data-management/preview/all`, { method: 'POST' });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },

  deleteOneComparison: async (id: number) => {
    const res = await fetch(`${BASE}/data-management/comparisons/${id}`, { method: 'DELETE' });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },

  deleteComparisonsByIds: async (ids: number[]) => {
    const res = await fetch(`${BASE}/data-management/comparisons`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comparison_ids: ids }),
    });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },

  deleteByDateRange: async (dateFrom: string, dateTo: string) => {
    const res = await fetch(`${BASE}/data-management/by-date-range`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date_from: dateFrom, date_to: dateTo }),
    });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },

  deleteAllComparisons: async () => {
    const res = await fetch(`${BASE}/data-management/all?confirmed=true`, { method: 'DELETE' });
    if (!res.ok) { const m = await res.text(); throw new Error(m); }
    return res.json();
  },
};
