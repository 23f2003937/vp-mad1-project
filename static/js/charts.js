// Chart.js configurations and functions for Parking Management System

// Chart.js default configuration
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.plugins.legend.display = true;
Chart.defaults.plugins.legend.position = 'bottom';

// Color palette for charts
const chartColors = {
    primary: '#0d6efd',
    secondary: '#6c757d',
    success: '#198754',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#0dcaf0',
    light: '#f8f9fa',
    dark: '#212529'
};

// Admin Charts
function loadAdminCharts() {
    // Load parking spots overview chart
    loadParkingSpotsChart();
    
    // Load parking lots distribution chart
    loadParkingLotsChart();
    
    // Load revenue chart
    loadRevenueChart();
    
    // Fetch data from API
    fetch('/api/admin/chart_data')
        .then(response => response.json())
        .then(data => {
            updateAdminCharts(data);
        })
        .catch(error => {
            console.error('Error loading admin chart data:', error);
        });
}

function loadParkingSpotsChart() {
    const ctx = document.getElementById('spotsChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Available', 'Occupied'],
            datasets: [{
                data: [0, 0], // Will be updated with real data
                backgroundColor: [chartColors.success, chartColors.danger],
                borderWidth: 2,
                borderColor: chartColors.dark
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: false
                }
            }
        }
    });
}

function loadParkingLotsChart() {
    const ctx = document.getElementById('lotsChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Occupied',
                data: [],
                backgroundColor: chartColors.danger,
                borderColor: chartColors.danger,
                borderWidth: 1
            }, {
                label: 'Available',
                data: [],
                backgroundColor: chartColors.success,
                borderColor: chartColors.success,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    grid: {
                        color: chartColors.light
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function loadRevenueChart() {
    const ctx = document.getElementById('revenueChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Revenue ($)',
                data: [],
                borderColor: chartColors.primary,
                backgroundColor: chartColors.primary + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: chartColors.light,
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: chartColors.light
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Revenue: $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

function updateAdminCharts(data) {
    // Update spots chart
    const spotsChart = Chart.getChart('spotsChart');
    if (spotsChart && data.lots) {
        const totalOccupied = data.lots.occupied.reduce((a, b) => a + b, 0);
        const totalAvailable = data.lots.available.reduce((a, b) => a + b, 0);
        
        spotsChart.data.datasets[0].data = [totalAvailable, totalOccupied];
        spotsChart.update();
    }
    
    // Update lots chart
    const lotsChart = Chart.getChart('lotsChart');
    if (lotsChart && data.lots) {
        lotsChart.data.labels = data.lots.names;
        lotsChart.data.datasets[0].data = data.lots.occupied;
        lotsChart.data.datasets[1].data = data.lots.available;
        lotsChart.update();
    }
    
    // Update revenue chart
    const revenueChart = Chart.getChart('revenueChart');
    if (revenueChart && data.revenue) {
        revenueChart.data.labels = data.revenue.dates;
        revenueChart.data.datasets[0].data = data.revenue.amounts;
        revenueChart.update();
    }
}

// User Charts
function loadUserCharts() {
    // Load user costs chart
    loadUserCostsChart();
    
    // Load user duration chart
    loadUserDurationChart();
    
    // Fetch data from API
    fetch('/api/user/chart_data')
        .then(response => response.json())
        .then(data => {
            updateUserCharts(data);
        })
        .catch(error => {
            console.error('Error loading user chart data:', error);
        });
}

function loadUserCostsChart() {
    const ctx = document.getElementById('userCostsChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Cost ($)',
                data: [],
                backgroundColor: chartColors.primary,
                borderColor: chartColors.primary,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: chartColors.light
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Cost: $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

function loadUserDurationChart() {
    const ctx = document.getElementById('userDurationChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Duration (hours)',
                data: [],
                borderColor: chartColors.info,
                backgroundColor: chartColors.info + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: chartColors.info,
                pointBorderColor: chartColors.light,
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: chartColors.light
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1) + 'h';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Duration: ' + context.parsed.y.toFixed(1) + ' hours';
                        }
                    }
                }
            }
        }
    });
}

function updateUserCharts(data) {
    // Update costs chart
    const costsChart = Chart.getChart('userCostsChart');
    if (costsChart) {
        costsChart.data.labels = data.dates || [];
        costsChart.data.datasets[0].data = data.costs || [];
        costsChart.update();
    }
    
    // Update duration chart
    const durationChart = Chart.getChart('userDurationChart');
    if (durationChart) {
        durationChart.data.labels = data.dates || [];
        durationChart.data.datasets[0].data = data.durations || [];
        durationChart.update();
    }
}

// Utility functions
function showChartLoading(chartId) {
    const canvas = document.getElementById(chartId);
    if (canvas) {
        canvas.classList.add('loading');
    }
}

function hideChartLoading(chartId) {
    const canvas = document.getElementById(chartId);
    if (canvas) {
        canvas.classList.remove('loading');
    }
}

// Error handling for charts
function showChartError(chartId, message) {
    const canvas = document.getElementById(chartId);
    if (canvas) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = chartColors.danger;
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(message || 'Error loading chart', canvas.width / 2, canvas.height / 2);
    }
}

// Responsive chart handling
function handleChartResize() {
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.resize();
    });
}

// Event listeners
window.addEventListener('resize', function() {
    setTimeout(handleChartResize, 100);
});

// Export functions for global use
window.loadAdminCharts = loadAdminCharts;
window.loadUserCharts = loadUserCharts;
window.updateAdminCharts = updateAdminCharts;
window.updateUserCharts = updateUserCharts;
