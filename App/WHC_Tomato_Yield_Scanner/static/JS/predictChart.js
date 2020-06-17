var ctx = document.getElementById('predictChart');
const healthy = document.getElementById('JS-healthy').textContent;
const unhealthy = document.getElementById('JS-unhealthy').textContent;
var data = {
    datasets: [{
        data: [healthy, unhealthy],
        backgroundColor: ['rgba(212, 237, 218, 1)', 'rgba(248, 215, 218, 1)'],
        borderColor: ['rgba(195, 230, 203, 1)', 'rgba(245, 198, 203, 1)']
    }],
    labels: [
        'Healthy',
        'Unhealthy'
    ]
}
var predictChart = new Chart(ctx, {
    type: 'pie',
    data: data
});