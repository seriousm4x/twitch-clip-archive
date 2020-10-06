function clips_in_month(data) {
    Chart.defaults.global.legend.display = false;
    data["datasets"][0]["backgroundColor"] = Chart['colorschemes'].tableau.Tableau10
    var ctx = document.getElementById('clips_in_month');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
};

function clips_by_category(data) {
    Chart.defaults.global.legend.display = true;
    var ctx = document.getElementById('clips_by_category');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                colorschemes: {
                    scheme: 'tableau.Tableau10'
                }
            }
        }
    });
};
