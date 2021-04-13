 var dates = {{data["prediction"]["xaxis"]}};
 var salesArray = {{data["prediction"]["yaxis"] | safe}};
 var arraySize = dates.length;

function invalidDate() {
    //TODO: Vamshi
    // function to make a error message visible
}

var ctx = document.getElementById('salesChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
//        labels: {{ data["prediction"]["xaxis"] | safe}},
        labels: dates,
        datasets: [{
            label: 'No. of items sold',
            fill: true,
            lineTension: 0,
//            data: {{ data["prediction"]["yaxis"] | safe }},
            data: salesArray,
            borderColor: "rgba(0, 0, 0, 1)",
            borderWidth: 1,

            pointBackgroudColor: "rgba(255, 0, 0, 1)"
        }]
    },

});

function setRange() {
    var from = reformatDate(document.getElementById('from-date').value);
    var to = reformatDate(document.getElementById('to-date').value);
    console.log(dates);
    console.log(from);
    console.log(to);
    try {
        var fromIndex = dates.indexOf(from);
        var toIndex = dates.indexOf(to);
    }catch(err){
        console.log(err);
        invalidDate();
        return;
    }
    myChart.data.labels = dates.slice(fromIndex, toIndex + 1);
    myChart.data.datasets[0].data = salesArray.slice(fromIndex, toIndex + 1);
    myChart.update();
}

var reformatDate = function(date) {
    dateArray = date.split('-');
    reformatted = dateArray[2] + '-' + dateArray[1] +'-'+dateArray[0];
    return reformatted;
}