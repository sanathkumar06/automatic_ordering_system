    var ctx = document.getElementById('salesChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{data["predictedSales"]["xaxis"] | safe}},
            datasets: [{
                label: 'Prediction',
                fill: true,
                lineTension: 0,
                data: {{ data["predictedSales"]["yaxis"] | safe}},

                borderColor: "rgba(0, 0, 255, 1)",
                borderWidth: 1,

                pointBackgroundColor: "rgba(255, 0, 0, 1)"
            },
            {
                label: 'No. of items sold',
                fill: true,
                lineTension: 0,
                data: {{ data["salesData"] | safe}},

                borderColor: "rgba(0, 0, 0, 1)",
                borderWidth: 1,

                pointBackgroundColor: "rgba(255, 0, 0, 1)"
            }]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        autoSkip: true,
                        beginAtZero: true,
                    }
                }]
            }
        }
    });