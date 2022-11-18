
$(function() {
    "use strict";

    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });
    $('.knob').knob({
        draw: function () {           
        }
    });

    // Current Ticket Status
    $(document).ready(function(){
        var chart = c3.generate({
            bindto: '#chart-combination', // id of chart wrapper
            data: {
                columns: [
                    // each columns data
                    ['data1', 1,2,4,9,6,3,2,5,8,7],
                    ['data2', 7,5,2,1,6,4,9,8,3,2],
                    ['data3', 7,5,3,1,5,9,8,5,2,6],
                    ['data4', 1,2,3,5,4,8,5,2,6,1],
                ],
                type: 'bar', // default type of chart
                types: {
                    'data2': "line",
                    'data3': "spline",
                },
                groups: [
                    [ 'data1', 'data4']
                ],
                colors: {
                    'data1': '#5a5278',
                    'data2': '#F2B335',
                    'data3': '#F2B335',
                    'data4': '#E74C3C'
                },
                names: {
                    // name of each serie
                    'data1': 'Development',
                    'data2': 'Marketing',
                    'data3': 'Design',
                    'data4': 'Sales'
                }
            },
            axis: {
                x: {
                    type: 'category',
                    // name of each category
                    categories: ['Jun 1','Jun 2','Jun 3','Jun 4','Jun 5','Jun 6','Jun 7','Jun 8','Jun 9','Jun 10']
                },
            },
            bar: {
                width: 16
            },
            legend: {
                show: false, //hide legend
            },
            padding: {
                bottom: 0,
                top: 0
            },
        });
    });

    // Area Datetime
    $(document).ready(function() {
        var options = {
            annotations: {
                yaxis: [{
                    y: 30,
                    borderColor: '#E74C3C',
                    label: {
                        show: true,
                        text: 'Support',
                        style: {
                            color: "#fff",
                            background: '#E74C3C'
                        }
                    }
                }],
                xaxis: [{
                    x: new Date('14 Nov 2012').getTime(),
                    borderColor: '#E74C3C',
                    yAxisIndex: 0,
                    label: {
                        show: true,
                        text: 'Sales',
                        style: {
                            color: "#fff",
                            background: '#E74C3C'
                        }
                    }
                }]
            },
            chart: {
                type: 'area',
                height: 350,
                toolbar: {
                    show: false,
                },
            },
            colors: ['#E74C3C'],
            dataLabels: {
                enabled: false
            },

            
            markers: {
                size: 0,
                style: 'hollow',
            },
            xaxis: {
                type: 'datetime',
                min: new Date('01 Mar 2012').getTime(),
                tickAmount: 6,
                show: false,
            },
            tooltip: {
                x: {
                    format: 'dd MMM yyyy'
                }
            },
            stroke: {
                show: true,
                curve: 'smooth',
                width: 1,
            },
            grid: {
                yaxis: {
                    lines: {
                        show: false,
                    }
                },
            },
        }





        var chart = new ApexCharts(
            document.querySelector("#apex-timeline-chart"),
            options
        );

        chart.render();

        var resetCssClasses = function (activeEl) {
            var els = document.querySelectorAll("button");
            Array.prototype.forEach.call(els, function (el) {
            el.classList.remove('active');
            });

            activeEl.target.classList.add('active')
        }

        document.querySelector("#one_month").addEventListener('click', function (e) {
            resetCssClasses(e)
            chart.updateOptions({
            xaxis: {
                min: new Date('28 Jan 2013').getTime(),
                max: new Date('27 Feb 2013').getTime(),
            }
            })
        })
        document.querySelector("#six_months").addEventListener('click', function (e) {
            resetCssClasses(e)
            chart.updateOptions({
            xaxis: {
                min: new Date('27 Sep 2012').getTime(),
                max: new Date('27 Feb 2013').getTime(),
            }
            })
        })
        document.querySelector("#one_year").addEventListener('click', function (e) {
            resetCssClasses(e)
            chart.updateOptions({
            xaxis: {
                min: new Date('27 Feb 2012').getTime(),
                max: new Date('27 Feb 2013').getTime(),
            }
            })
        })
        document.querySelector("#ytd").addEventListener('click', function (e) {
            resetCssClasses(e)
            chart.updateOptions({
            xaxis: {
                min: new Date('01 Jan 2013').getTime(),
                max: new Date('27 Feb 2013').getTime(),
            }
            })
        })
        document.querySelector("#all").addEventListener('click', function (e) {
            resetCssClasses(e)
            chart.updateOptions({
            xaxis: {
                min: undefined,
                max: undefined,
            }
            })
        })
        document.querySelector("#ytd").addEventListener('click', function () {

        })
    });

});