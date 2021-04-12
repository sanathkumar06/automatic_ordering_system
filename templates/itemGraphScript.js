 var dates = data["dates"];
 var salesArray = data["sales"];
 var arraySize = dates.length;

function invalidDate() {
    //todo: Vamshi
    // function to make a error message visible
}

var ctx = document.getElementById('salesChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: '{{ data["prediction"]["xaxis"] }}',
           labels: dates,
        datasets: [{
            label: 'No. of items sold',
            fill: true,
            lineTension: 0,
            data: '{{ data["prediction"]["yaxis"] }}',
            data: salesArray,

            borderColor: "rgba(0, 0, 0, 1)",
            borderWidth: 1,
            pointBackgroudColor: "rgba(255, 0, 0, 1)"
        }]
    },
    options: {
        scales: {
            xAxes: [{
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 15
                }
            }],
            yAxes: [{
                ticks: {
                    autoSkip: true,
                    beginAtZero: true
                }
            }]
        }
    }
});

function setRange() {
    var from = document.getElementById('from-date');
    var to = document.getElementById('to-date');
    try {
        var fromIndex = dates.findIndex(from);
        var toIndex = dates.findIndex(to);
    }catch(err){
        console.log(err);
        invalidDate();
        return;
    }
    myChart.data.labels = dates.slice(fromIndex, toIndex + 1);
    myChart.data.datasets[0].data = salesArray.slice(fromIndex, toIndex + 1);
    myChart.update();
}