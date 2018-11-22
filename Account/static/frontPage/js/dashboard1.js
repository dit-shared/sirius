
$(function() {
    // ============================================================== 
    // Sales overview
    // ============================================================== 
    Morris.Area({
        element: 'earning',
        data: [{
                month: '2017-12',
                Cold: 6.1,
                Hot: 4.4,
            },{
                month: '2018-01',
                Cold: 7.8,
                Hot: 5.1,
            },{
                month: '2018-02',
                Cold: 7.3,
                Hot: 4.8,
            },{
                month: '2018-03',
                Cold: 5.4,
                Hot: 5.0,
            },{
                month: '2018-04',
                Cold: 7.1,
                Hot: 4.6,
            },{
                month: '2018-05',
                Cold: 6.3,
                Hot: 5.2,
            },{
                month: '2018-06',
                Cold: 9.0,
                Hot: 6.5,
            },{
                month: '2018-07',
                Cold: 9.2,
                Hot: 4.2,
            },{
                month: '2018-08',
                Cold: 6.4,
                Hot: 4.8,
            },{
                month: '2018-09',
                Cold: 6.1,
                Hot: 5.1,
            },{
                month: '2018-10',
                Cold: 6.9,
                Hot: 6.2,
            },
        ],
        xkey: 'month',
        ykeys: ['Hot', 'Cold'],
        labels: ['Горячая', 'Холодная'],
        pointSize: 3,
        fillOpacity: 0,
        pointStrokeColors: ['#1976d2', '#26c6da', '#1976d2'],
        behaveLikeLine: true,
        gridLineColor: '#e0e0e0',
        lineWidth: 3,
        hideHover: 'auto',
        lineColors: ['#FF8080', '#007bff',],
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