import { Chart, registerables } from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

Chart.register(...registerables);

const commonLegend = {
  position: 'bottom' as const,
  labels: {
    color: '#54657A',
    usePointStyle: true,
    pointStyle: 'circle',
    boxWidth: 10,
    boxHeight: 10,
    padding: 18,
    font: {
      family: 'IBM Plex Sans',
      size: 12,
      weight: '600',
    },
  },
};

const sharedTooltip = {
  backgroundColor: '#172A36',
  titleColor: '#F6F4EE',
  bodyColor: '#F6F4EE',
  borderColor: 'rgba(255,255,255,0.08)',
  borderWidth: 1,
  padding: 10,
  displayColors: true,
};

export function BarChart({ title, labels, ai, human, aiLabel = 'AI', humanLabel = 'Human' }: any) {
  const data = {
    labels,
    datasets: [
      {
        label: aiLabel,
        data: ai,
        backgroundColor: '#2F6A8E',
        borderRadius: 8,
        borderSkipped: false,
        borderColor: 'rgba(47,106,142,0.45)',
        borderWidth: 1,
      },
      {
        label: humanLabel,
        data: human,
        backgroundColor: '#B86C2A',
        borderRadius: 8,
        borderSkipped: false,
        borderColor: 'rgba(184,108,42,0.45)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 500, easing: 'easeOutQuart' },
    layout: { padding: { top: 6, right: 12, left: 8, bottom: 0 } },
    plugins: {
      legend: commonLegend,
      tooltip: sharedTooltip,
      title: {
        display: !!title,
        text: title,
        color: '#1F3347',
        padding: { top: 0, bottom: 12 },
        font: {
          family: 'IBM Plex Sans',
          size: 13,
          weight: '700',
        },
      },
    },
    scales: {
      x: {
        grid: { display: false, drawBorder: false },
        ticks: {
          color: '#54657A',
          font: { family: 'IBM Plex Sans', size: 11, weight: '600' },
        },
      },
      y: {
        beginAtZero: true,
        suggestedMax: 100,
        grid: {
          color: 'rgba(23,42,54,0.08)',
          drawBorder: false,
        },
        ticks: {
          color: '#54657A',
          stepSize: 25,
          font: { family: 'IBM Plex Sans', size: 11 },
        },
      },
    },
  };

  return (
    <div style={{ position: 'relative', height: 240 }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export function DoughnutChart({ title, labels, values, colors }: any) {
  const data = { labels, datasets: [{ data: values, backgroundColor: colors, borderColor: '#ffffff', borderWidth: 2, hoverOffset: 4 }] };
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '58%',
    plugins: {
      legend: commonLegend,
      tooltip: sharedTooltip,
      title: {
        display: !!title,
        text: title,
        color: '#1F3347',
        padding: { top: 0, bottom: 12 },
        font: {
          family: 'IBM Plex Sans',
          size: 13,
          weight: '700',
        },
      },
    },
  };

  return (
    <div style={{ position: 'relative', height: 240 }}>
      <Doughnut data={data} options={options} />
    </div>
  );
}
