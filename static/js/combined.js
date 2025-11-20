let miniLSChart, miniFLChart, miniCombinedChart;

function createMiniChart(ctx, color) {
    return new Chart(ctx, {
        type: 'line',
        data: { labels: [], datasets: [{ label: '', data: [] }] },
        options: {
            animation: { duration: 500, easing: 'easeInOutQuart' },
            plugins: { legend: { display: false } },
            scales: { x: { display: false }, y: { display: false } }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    miniLSChart = createMiniChart(document.getElementById("miniLS").getContext("2d"));
    miniFLChart = createMiniChart(document.getElementById("miniFL").getContext("2d"));
    miniCombinedChart = createMiniChart(document.getElementById("miniCombined").getContext("2d"));

    updateCombined();
    setInterval(updateCombined, 1200);
});

async function updateCombined() {
    const [respC, respN] = await Promise.all([fetch("/api/combined"), fetch("/api/notifications")]);
    const dC = await respC.json();
    const notifs = await respN.json();

    const ls = dC.landslide;
    const fl = dC.flood;
    const comb = dC.combined;

    setRiskBox(document.getElementById("landslideRisk"), ls);
    setRiskBox(document.getElementById("floodRisk"), fl);
    setRiskBox(document.getElementById("combinedRisk"), comb);

    // push to mini charts
    pushAndCap(miniLSChart.data.labels, dC.timestamp);
    pushAndCap(miniLSChart.data.datasets[0].data, ls);
    miniLSChart.update();

    pushAndCap(miniFLChart.data.labels, dC.timestamp);
    pushAndCap(miniFLChart.data.datasets[0].data, fl);
    miniFLChart.update();

    pushAndCap(miniCombinedChart.data.labels, dC.timestamp);
    pushAndCap(miniCombinedChart.data.datasets[0].data, comb);
    miniCombinedChart.update();

    // notifications
    const ul = document.getElementById("globalNotif");
    ul.innerHTML = "";
    notifs.slice().reverse().forEach(n => {
        const li = document.createElement("li");
        li.textContent = `[${n.time}] ${n.msg}`;
        ul.appendChild(li);
    });
}
