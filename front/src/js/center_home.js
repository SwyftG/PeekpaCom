$(document).ready(function () {
    var loadingCircle = $('#loading-circle');
    var rowOneLeft = $('#row-1-left');
    var rowOneRight = $('#row-1-right');
    rowOneLeft.hide();
    rowOneRight.hide();
    loadingCircle.show();
    var $caoliuChart = $('#caoliu-post-chart');
    var $javpopChart = $('#jav-post-chart');
    $.ajax({
        url: "/center/dashboard",
        type: "get",
        success: function (data) {
            console.log(data)
            loadingCircle.hide();
            rowOneLeft.show();
            rowOneRight.show();

            var ticksStyle = {
                fontColor: '#495057',
                fontStyle: 'bold'
            }
            var mode = 'index'
            var intersect = true

            var cahliuPostChart = new Chart($caoliuChart, {
                type: 'bar',
                data: {
                    labels: ['技术讨论', '亚洲五码', '亚洲有码', '欧美专场', '中文原创', '国产原创'],
                    datasets: [
                        {
                            backgroundColor: '#007bff',
                            borderColor: '#007bff',
                            data: data['today_caoliu_data_list']
                        },
                        {
                            backgroundColor: '#ced4da',
                            borderColor: '#ced4da',
                            data: data['yesterday_caoliu_data_list']
                        }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        mode: mode,
                        intersect: intersect
                    },
                    hover: {
                        mode: mode,
                        intersect: intersect
                    },
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            // display: false,
                            gridLines: {
                                display: true,
                                lineWidth: '4px',
                                color: 'rgba(0, 0, 0, .2)',
                                zeroLineColor: 'transparent'
                            },
                            ticks: $.extend({
                                beginAtZero: true,
                            }, ticksStyle)
                        }],
                        xAxes: [{
                            display: true,
                            gridLines: {
                                display: false
                            },
                            ticks: ticksStyle
                        }]
                    }
                }
            });


            var javPostChart = new Chart($javpopChart, {
                type: 'bar',
                data: {
                    labels: ['写真电影', '有码电影', '无码电影'],
                    datasets: [
                        {
                            backgroundColor: '#007bff',
                            borderColor: '#007bff',
                            data: data['today_javpop_data_list']
                        },
                        {
                            backgroundColor: '#ced4da',
                            borderColor: '#ced4da',
                            data: data['yesterday_javpop_data_list']
                        }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        mode: mode,
                        intersect: intersect
                    },
                    hover: {
                        mode: mode,
                        intersect: intersect
                    },
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            // display: false,
                            gridLines: {
                                display: true,
                                lineWidth: '4px',
                                color: 'rgba(0, 0, 0, .2)',
                                zeroLineColor: 'transparent'
                            },
                            ticks: $.extend({
                                beginAtZero: true,
                            }, ticksStyle)
                        }],
                        xAxes: [{
                            display: true,
                            gridLines: {
                                display: false
                            },
                            ticks: ticksStyle
                        }]
                    }
                }
            });
            var topActressBlock = $("#top-actress-block");
            var tpl = template('data-list', {'data': data} );
            topActressBlock.append(tpl);
        }
    })
});

