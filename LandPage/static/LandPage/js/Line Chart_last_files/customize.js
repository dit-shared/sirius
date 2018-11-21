var MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
            var config = {
                type: 'line',
                data: {
                    labels: ['Декабрь', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Сентябрь', 'Октябрь', 'Ноябрь'],
                    datasets: [{
                        label: 'Горячая',
                        backgroundColor: window.chartColors.red,
                        borderColor: window.chartColors.red,
                        data: [
                        8.1,
                        4.9,
                        5.1,
                        6.4,
                        7.1,
                        6.5,
                        5.3,
						6.2,
						7.4,
						5.8						
                        ],
                        fill: false,
                    }, {
                        label: 'Холодная',
                        fill: false,
                        backgroundColor: window.chartColors.blue,
                        borderColor: window.chartColors.blue,
                        data: [
                        11.7,
                        7.2,
                        8.0,
                        9.2,
                        9.9,
                        10.2,
                        13.4,
						9.8,
						10.4,
						8.9						
                        ],
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Расход воды'
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false,
                    },
                    hover: {
                        mode: 'nearest',
                        intersect: true
                    },
                    scales: {
                        xAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Месяц'
                            }
                        }],
                        yAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Расход'
                            }
                        }]
                    }
                }
            };

            window.onload = function() {
                var ctx = document.getElementById('canvas').getContext('2d');
                window.myLine = new Chart(ctx, config);
            };

            document.getElementById('randomizeData').addEventListener('click', function() {
                config.data.datasets.forEach(function(dataset) {
                    dataset.data = dataset.data.map(function() {
                        return randomScalingFactor();
                    });

                });

                window.myLine.update();
            });

            var colorNames = Object.keys(window.chartColors);
            document.getElementById('addDataset').addEventListener('click', function() {
                var colorName = colorNames[config.data.datasets.length % colorNames.length];
                var newColor = window.chartColors[colorName];
                var newDataset = {
                    label: 'Dataset ' + config.data.datasets.length,
                    backgroundColor: newColor,
                    borderColor: newColor,
                    data: [],
                    fill: false
                };

                for (var index = 0; index < config.data.labels.length; ++index) {
                    newDataset.data.push(randomScalingFactor());
                }

                config.data.datasets.push(newDataset);
                window.myLine.update();
            });

            document.getElementById('addData').addEventListener('click', function() {
                if (config.data.datasets.length > 0) {
                    var month = MONTHS[config.data.labels.length % MONTHS.length];
                    config.data.labels.push(month);

                    config.data.datasets.forEach(function(dataset) {
                        dataset.data.push(randomScalingFactor());
                    });

                    window.myLine.update();
                }
            });

            document.getElementById('removeDataset').addEventListener('click', function() {
                config.data.datasets.splice(0, 1);
                window.myLine.update();
            });

            document.getElementById('removeData').addEventListener('click', function() {
                config.data.labels.splice(-1, 1); // remove the label first

                config.data.datasets.forEach(function(dataset) {
                    dataset.data.pop();
                });

                window.myLine.update();
            });