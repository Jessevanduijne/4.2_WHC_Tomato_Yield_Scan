const unique_id = document.getElementById("JS-unique_id").textContent;
const historyData = JSON.parse(document.getElementById("JS-healthy_percentages").textContent)
const historyLabels = JSON.parse(document.getElementById("JS-unique_ids").textContent)

var ctx = document.getElementById("historyChart");
var historyChart = new Chart(ctx.getContext("2d"), {
    "type": "line", 
    "data": { 
        "labels": historyLabels,
        "datasets": [{ 
            "label": "Latest Results", 
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
                radius: highlighted,
                display: true
            }
        }
    }
});

function highlighted(context) {
    var index = context.dataIndex;

    return historyLabels[index] === unique_id ? 10 : 2;
}

ctx.onclick = function(e) {
    var point = historyChart.getElementAtEvent(e)[0];
    window.location = "/results/"+historyLabels[point._index];
};