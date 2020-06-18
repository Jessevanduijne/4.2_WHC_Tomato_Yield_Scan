const unique_id = document.getElementById("JS-unique_id").textContent;
const historyData = JSON.parse(document.getElementById("JS-healthy_percentages").textContent)
const historyLabels = JSON.parse(document.getElementById("JS-unique_ids").textContent)

var ctx = document.getElementById("historyChart");
var historyChart = new Chart(ctx.getContext("2d"), {
    "type": "line", 
    "data": { 
        "labels": historyLabels,
        "datasets": [{ 
            "label": "Your Latest Results", 
            "data": historyData, 
            "fill": false,
            "borderColor": "rgb(75, 192, 192)", 
        }] 
    }, 
    options: {
        scales: {
            xAxes: [{
                ticks: {
                    display: false
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
                label: function(tooltipItem, data) {
                    return "Healthy Yield: " + tooltipItem.value;
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