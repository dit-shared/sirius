
$(function() {
    // ============================================================== 
    // Sales overview
    // ============================================================== 
    Morris.Area({
        element: 'electricity',
        data: [{
                month: '2017-12',
                Cold: 83,
                Hot: 31,
            },{
                month: '2018-01',
                Cold: 98,
                Hot: 29,
            },{
                month: '2018-02',
                Cold: 145,
                Hot: 47,
            },{
                month: '2018-03',
                Cold: 95,
                Hot: 28,
            },{
                month: '2018-04',
                Cold: 51,
                Hot: 24,
            },{
                month: '2018-05',
                Cold: 58,
                Hot: 20,
            },{
                month: '2018-06',
                Cold: 112,
                Hot: 44,
            },{
                month: '2018-07',
                Cold: 54,
                Hot: 21,
            },{
                month: '2018-08',
                Cold: 79,
                Hot: 33,
            },{
                month: '2018-09',
                Cold: 56,
                Hot: 32,
            },{
                month: '2018-10',
                Cold: 55,
                Hot: 21,
            },
        ],
        xkey: 'month',
        ykeys: ['Hot', 'Cold'],
        labels: ['Ночь', 'Пик'],
        pointSize: 3,
        fillOpacity: 0,
        pointStrokeColors: ['#1976d2', '#26c6da', '#1976d2'],
        behaveLikeLine: true,
        gridLineColor: '#e0e0e0',
        lineWidth: 3,
        hideHover: 'auto',
        lineColors: ['#000000', '#ff6600',],
        resize: true,
        xLabelAngle: 45,
        xLabels: 'month',
    });

    // ============================================================== 
    // Sales overview
    // ==============================================================
    // ============================================================== 
    // Download count
    // ============================================================== 
    var sparklineLogin = function() {
        $('.spark-count').sparkline([4, 5, 0, 10, 9, 12, 4, 9, 4, 5, 3, 10, 9, 12, 10, 9], {
            type: 'bar',
            width: '100%',
            height: '70',
            barWidth: '2',
            resize: true,
            barSpacing: '6',
            barColor: 'rgba(255, 255, 255, 0.3)'
        });

        $('.spark-count2').sparkline([20, 40, 30], {
            type: 'pie',
            height: '80',
            resize: true,
            sliceColors: ['#1cadbf', '#1f5f67', '#ffffff']
        });
    }
    var sparkResize;

    sparklineLogin();


});