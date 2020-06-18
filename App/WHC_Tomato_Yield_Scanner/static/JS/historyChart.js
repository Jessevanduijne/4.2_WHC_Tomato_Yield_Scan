const unique_id = document.getElementById("JS-unique_id").textContent;
const historyData = JSON.parse(document.getElementById("JS-healthy_percentages").textContent)
const historyLabels = JSON.parse(document.getElementById("JS-unique_ids").textContent)
const resultDates = JSON.parse(document.getElementById("JS-result_dates").textContent)

var ctx = document.getElementById("historyChart");
var historyChart = new Chart(ctx.getContext("2d"), {
    "type": "line", 
    "data": { 
        "datasets": [{ 
            "label": "Your Latest Results", 
            "data": makeChartData(), 
            "fill": false,
            "borderColor": "rgb(75, 192, 192)", 
        }] 
    }, 
    options: {
        scales: {
            xAxes: [{
                type: "time",
                distribution: "series",
            }],
            yAxes: [{
                ticks: {
                    suggestedMin: 0,
                    beginAtZero: true,
                    suggestedMax: 100,
                }
            }]
        },
        elements: {
            point: {
                radius: function (context) {
                    var index = context.dataIndex;
                
                    return historyLabels[index] === unique_id ? 10 : 2;
                },
                display: true
            }
        },
        tooltips: {
            callbacks: {
                title: function(tooltipItem, data) {
                    return historyLabels[tooltipItem[0].index];
                },
                label: function(tooltipItem, data) {
                    return "Healthy Yield: " + tooltipItem.value + "%";
                }
            }
        }
    }
});

ctx.onclick = function(e) {
    var point = historyChart.getElementAtEvent(e)[0];
    var pointUniqueId = historyLabels[point._index];
    
    if (unique_id !== pointUniqueId) {
        window.location = "/results/"+pointUniqueId;
    }
};

function makeChartData() {
    var chartData = [];
    for (i = 0; i < historyData.length; i++) {
        chartData.push({
            x: new Date(resultDates[i]),
            y: historyData[i]
        });
    }
    return chartData;
};