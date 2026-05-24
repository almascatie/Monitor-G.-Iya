async function loadData() {

  const latest = await fetch('data/latest.json').then(r => r.json());
  const analysis = await fetch('data/analysis.json').then(r => r.json());
  const history = await fetch('data/history.json').then(r => r.json());

  document.getElementById('status').innerText = latest.status;

  document.getElementById('analysis').innerText = analysis.summary;

  document.getElementById('risk-score').innerText = analysis.risk_score;

  const historyList = document.getElementById('history-list');

  history.slice(0, 10).forEach(item => {
    const li = document.createElement('li');
    li.innerText = `${item.date} - ${item.status}`;
    historyList.appendChild(li);
  });

  const labels = history.map(h => h.date).reverse();
  const values = history.map(h => h.gempa).reverse();

  const ctx = document.getElementById('activityChart');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Jumlah Gempa',
        data: values,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true
    }
  });
}

loadData();
