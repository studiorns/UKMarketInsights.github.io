// UK Market Data
const ukData = {
    impressions: {
        '2023': [39266229, 57795441, 100046948, 25065565, 30007835, 20505990, 20370260, 47983271, 22843633, 35095789, 105077019, 151167994],
        '2024': [39767259, 20577624, 50003357, 109331811, 45176614, 37914837, 56385822, 30416431, 55798934, 111534185, 136058361, 47304711],
        '2025': [63743254, 70187219, 119431507, 149301104, 96899625, 64959531, 63978941, 63978941, 45474202, 51467010, 100082976, 83358485]
    },
    travelQueries: {
        '2023': [89.36, 73.07, 79.49, 91.35, 76.72, 71.75, 86.36, 86.07, 89.66, 102.53, 90.83, 91.73],
        '2024': [124.85, 98.80, 99.09, 92.34, 86.94, 82.80, 86.15, 92.83, 99.68, 110.86, 97.25, 99.18],
        '2025': {
            'moderate': [140.09, 116.37, 121.81, 97.33, 88.33, 80.16, 84.87, 95.97, 116.99, 141.94, 107.87, 121.92],
            'conservative': [132.84, 110.31, 115.46, 92.27, 83.75, 75.98, 80.44, 90.96, 110.90, 134.59, 102.26, 115.57],
            'ambitious': [147.34, 122.43, 128.15, 102.38, 92.92, 84.35, 89.30, 100.97, 123.07, 149.28, 113.49, 128.28]
        }
    },
    flightSearches: {
        '2023': [10767, 6511, 7372, 6642, 6345, 6479, 9945, 9989, 10744, 11213, 12135, 11526],
        '2024': [17665, 13368, 15826, 13953, 17633, 17415, 20346, 15218, 22007, 19997, 12760, 15876]
    },
    hotelGuests: {
        '2023': [12304, 13858, 12817, 12797, 11185, 8253, 7009, 9876, 9170, 18296, 17845, 17082],
        '2024': [14154, 19770, 16710, 19461, 17258, 12160, 13222, 17891, 14968, 24484, 20531, 28534]
    }
};

// Months labels
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// Chart instances
let queriesChart, impressionsChart, flightsChart, hotelChart;

// Chart configuration
const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
        mode: 'index',
        intersect: false
    },
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                usePointStyle: true,
                padding: 15,
                font: {
                    family: "'Inter', sans-serif",
                    size: 12
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleFont: {
                family: "'Inter', sans-serif",
                weight: 'bold',
                size: 13
            },
            bodyFont: {
                family: "'Inter', sans-serif",
                size: 13
            },
            padding: 12,
            cornerRadius: 8,
            displayColors: true,
            usePointStyle: true,
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                        label += ': ';
                    }
                    if (context.parsed.y !== null) {
                        if (context.parsed.y > 1000000) {
                            label += (context.parsed.y / 1000000).toFixed(1) + 'M';
                        } else if (context.parsed.y > 1000) {
                            label += (context.parsed.y / 1000).toFixed(1) + 'K';
                        } else {
                            label += context.parsed.y.toLocaleString();
                        }
                    }
                    return label;
                }
            }
        }
    },
    scales: {
        x: {
            grid: {
                color: 'rgba(0, 0, 0, 0.05)'
            },
            ticks: {
                font: {
                    family: "'Inter', sans-serif",
                    size: 12
                }
            }
        },
        y: {
            beginAtZero: true,
            grid: {
                color: 'rgba(0, 0, 0, 0.05)'
            },
            ticks: {
                font: {
                    family: "'Inter', sans-serif",
                    size: 12
                }
            }
        }
    },
    elements: {
        line: {
            tension: 0.3
        },
        point: {
            radius: 3,
            hoverRadius: 6
        }
    },
    animation: {
        duration: 1000,
        easing: 'easeOutQuart'
    }
};

// Initialize charts
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    setupTabSwitching();
    setupScenarioButtons();
    setupPrintButton();
});

function initCharts() {
    // Travel Queries Chart
    const queriesCtx = document.getElementById('queries-chart').getContext('2d');
    queriesChart = new Chart(queriesCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: '2024 Actual',
                    data: ukData.travelQueries['2024'],
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: '2025 Moderate (+16.8%)',
                    data: ukData.travelQueries['2025']['moderate'],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            ...chartConfig,
            plugins: {
                ...chartConfig.plugins,
                title: {
                    display: true,
                    text: 'UK Travel Queries Forecast',
                    font: {
                        family: "'Inter', sans-serif",
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            },
            scales: {
                ...chartConfig.scales,
                y: {
                    ...chartConfig.scales.y,
                    title: {
                        display: true,
                        text: 'Travel Queries Index',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                },
                x: {
                    ...chartConfig.scales.x,
                    title: {
                        display: true,
                        text: 'Month',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                }
            }
        }
    });
    
    // Impressions Chart
    const impressionsCtx = document.getElementById('impressions-chart').getContext('2d');
    impressionsChart = new Chart(impressionsCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: '2023',
                    data: ukData.impressions['2023'],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: '2024',
                    data: ukData.impressions['2024'],
                    borderColor: 'rgba(255, 206, 86, 1)',
                    backgroundColor: 'rgba(255, 206, 86, 0.1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: '2025 (Planned)',
                    data: ukData.impressions['2025'],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            ...chartConfig,
            plugins: {
                ...chartConfig.plugins,
                title: {
                    display: true,
                    text: 'UK Media Impressions',
                    font: {
                        family: "'Inter', sans-serif",
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            },
            scales: {
                ...chartConfig.scales,
                y: {
                    ...chartConfig.scales.y,
                    title: {
                        display: true,
                        text: 'Impressions',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
                            if (value >= 1000) return (value / 1000).toFixed(1) + 'K';
                            return value;
                        }
                    }
                },
                x: {
                    ...chartConfig.scales.x,
                    title: {
                        display: true,
                        text: 'Month',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                }
            }
        }
    });
    
    // Flight Searches Chart
    const flightsCtx = document.getElementById('flights-chart').getContext('2d');
    flightsChart = new Chart(flightsCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: '2023',
                    data: ukData.flightSearches['2023'],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: '2024',
                    data: ukData.flightSearches['2024'],
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            ...chartConfig,
            plugins: {
                ...chartConfig.plugins,
                title: {
                    display: true,
                    text: 'UK Flight Searches',
                    font: {
                        family: "'Inter', sans-serif",
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            },
            scales: {
                ...chartConfig.scales,
                y: {
                    ...chartConfig.scales.y,
                    title: {
                        display: true,
                        text: 'Flight Searches',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                },
                x: {
                    ...chartConfig.scales.x,
                    title: {
                        display: true,
                        text: 'Month',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                }
            }
        }
    });
    
    // Hotel Guests Chart
    const hotelCtx = document.getElementById('hotel-chart').getContext('2d');
    hotelChart = new Chart(hotelCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: '2023',
                    data: ukData.hotelGuests['2023'],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: '2024',
                    data: ukData.hotelGuests['2024'],
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            ...chartConfig,
            plugins: {
                ...chartConfig.plugins,
                title: {
                    display: true,
                    text: 'UK Hotel Guests',
                    font: {
                        family: "'Inter', sans-serif",
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            },
            scales: {
                ...chartConfig.scales,
                y: {
                    ...chartConfig.scales.y,
                    title: {
                        display: true,
                        text: 'Hotel Guests',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                },
                x: {
                    ...chartConfig.scales.x,
                    title: {
                        display: true,
                        text: 'Month',
                        font: {
                            family: "'Inter', sans-serif",
                            weight: 'bold',
                            size: 13
                        }
                    }
                }
            }
        }
    });
}

function setupTabSwitching() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update active tab content
            const tabId = this.getAttribute('data-tab');
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
}

function setupScenarioButtons() {
    const scenarioButtons = document.querySelectorAll('.scenario-btn');
    scenarioButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active button
            scenarioButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update chart based on selected scenario
            updateQueriesChart(this.getAttribute('data-scenario'));
        });
    });
}

function updateQueriesChart(scenario) {
    // Clear existing datasets
    queriesChart.data.datasets = [];
    
    if (scenario === 'actual') {
        // Show 2023 and 2024 actual data
        queriesChart.data.datasets.push({
            label: '2023 Actual',
            data: ukData.travelQueries['2023'],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            borderWidth: 2,
            fill: false
        });
        
        queriesChart.data.datasets.push({
            label: '2024 Actual',
            data: ukData.travelQueries['2024'],
            borderColor: 'rgba(255, 159, 64, 1)',
            backgroundColor: 'rgba(255, 159, 64, 0.1)',
            borderWidth: 2,
            fill: false
        });
    } else {
        // Show 2024 actual and 2025 forecast for selected scenario
        queriesChart.data.datasets.push({
            label: '2024 Actual',
            data: ukData.travelQueries['2024'],
            borderColor: 'rgba(255, 159, 64, 1)',
            backgroundColor: 'rgba(255, 159, 64, 0.1)',
            borderWidth: 2,
            fill: false
        });
        
        let growthLabel = '';
        switch(scenario) {
            case 'conservative':
                growthLabel = ' (+10.8%)';
                break;
            case 'moderate':
                growthLabel = ' (+16.8%)';
                break;
            case 'ambitious':
                growthLabel = ' (+22.5%)';
                break;
        }
        
        queriesChart.data.datasets.push({
            label: `2025 ${scenario.charAt(0).toUpperCase() + scenario.slice(1)}${growthLabel}`,
            data: ukData.travelQueries['2025'][scenario],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            borderWidth: 2,
            fill: false
        });
    }
    
    // Update chart
    queriesChart.update();
}

function setupPrintButton() {
    const printBtn = document.querySelector('.print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    const exportBtn = document.querySelector('.export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            // Export functionality would go here
            alert('Export functionality would be implemented here.');
        });
    }
}
