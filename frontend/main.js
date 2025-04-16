// Loads and displays sample data. Replace fetch('sample_data.json') with API call for backend integration.
document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/api/transactions')
        .then(res => res.json())
        .then(data => {
            window.transactions = data;
            populateFilters(data);
            renderTable(data);
            renderTypeChart(data);
            renderMonthlyChart(data);
        });

    document.getElementById('typeFilter').addEventListener('change', filterAndRender);
    document.getElementById('dateFilter').addEventListener('change', filterAndRender);
    document.getElementById('amountFilter').addEventListener('input', filterAndRender);
    document.getElementById('resetFilters').addEventListener('click', function() {
        document.getElementById('typeFilter').value = '';
        document.getElementById('dateFilter').value = '';
        document.getElementById('amountFilter').value = '';
        filterAndRender();
    });

    function filterAndRender() {
        let filtered = window.transactions;
        const type = document.getElementById('typeFilter').value;
        const date = document.getElementById('dateFilter').value;
        const amount = parseInt(document.getElementById('amountFilter').value);
        if (type) filtered = filtered.filter(t => t.category === type);
        if (date) filtered = filtered.filter(t => t.date && t.date.startsWith(date));
        if (!isNaN(amount)) filtered = filtered.filter(t => t.amount >= amount);
        renderTable(filtered);
        renderTypeChart(filtered);
        renderMonthlyChart(filtered);
    }

    function populateFilters(data) {
        const types = [...new Set(data.map(t => t.category))];
        const typeSelect = document.getElementById('typeFilter');
        types.forEach(type => {
            const opt = document.createElement('option');
            opt.value = type;
            opt.textContent = type.replace(/_/g, ' ');
            typeSelect.appendChild(opt);
        });
    }

    function renderTable(data) {
        const tbody = document.querySelector('#transactionsTable tbody');
        tbody.innerHTML = '';
        data.forEach(tr => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${tr.id}</td><td>${tr.category}</td><td>${tr.amount}</td><td>${tr.sender||''}</td><td>${tr.receiver||''}</td><td>${tr.date||''}</td><td>${tr.description||''}</td>`;
            row.addEventListener('click', () => showDetails(tr));
            tbody.appendChild(row);
        });
    }

    function renderTypeChart(data) {
        const ctx = document.getElementById('typeChart').getContext('2d');
        if (window.typeChart) window.typeChart.destroy();
        const counts = {};
        data.forEach(tr => { counts[tr.category] = (counts[tr.category]||0)+1; });
        window.typeChart = new Chart(ctx, {
            type: 'bar',
            data: { labels: Object.keys(counts), datasets: [{ label: 'Count by Type', data: Object.values(counts), backgroundColor: '#4e79a7' }] },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }

    function renderMonthlyChart(data) {
        const ctx = document.getElementById('monthlyChart').getContext('2d');
        if (window.monthlyChart) window.monthlyChart.destroy();
        const monthly = {};
        data.forEach(tr => {
            if (tr.date) {
                const month = tr.date.slice(0,7);
                monthly[month] = (monthly[month]||0) + tr.amount;
            }
        });
        window.monthlyChart = new Chart(ctx, {
            type: 'line',
            data: { labels: Object.keys(monthly), datasets: [{ label: 'Volume by Month', data: Object.values(monthly), fill: false, borderColor: '#f28e2b' }] },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }

    // Modal for details
    const modal = document.getElementById('detailsModal');
    const close = document.querySelector('.close');
    close.onclick = () => modal.style.display = 'none';
    window.onclick = function(event) { if (event.target == modal) modal.style.display = 'none'; };
    function showDetails(tr) {
        document.getElementById('detailsContent').textContent = JSON.stringify(tr, null, 2);
        modal.style.display = 'block';
    }
});
