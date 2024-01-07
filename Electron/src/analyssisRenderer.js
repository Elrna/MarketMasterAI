document.addEventListener('DOMContentLoaded', () => {
    // データのリクエストを定期的に実行
    window.electronAPI.sendData('request-LSTM_output');
    setInterval(() => {
        try {
            window.electronAPI.sendData('request-LSTM_output');
        } catch (error) {
            console.error('Error sending data request:', error);
        }
    }, 50000); // 5秒ごとに設定

    window.electronAPI.receiveData('response-LSTM_output', (data) => {
        try {
            updateChart(data);
        } catch (error) {
            console.error('Error updating chart:', error);
        }
    });
});

let chart; // グローバル変数としてチャートを保持

function createChart(csvData) {
    const labels = csvData.map(row => row.timestamp);
    const chartData = csvData.map(row => parseFloat(row.close));

    const ctx = document.getElementById('LSTMoutput').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'LSTM output',
                data: chartData,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function updateChart(csvData) {
    if (!csvData || !Array.isArray(csvData) || csvData.length === 0) {
        throw new Error('Invalid or empty CSV data');
    }

    if (!chart) {
        createChart(csvData);
    } else {
        chart.data.labels = csvData.map(row => row.timestamp);
        chart.data.datasets[0].data = csvData.map(row => parseFloat(row.close));
        chart.update();
    }
}
