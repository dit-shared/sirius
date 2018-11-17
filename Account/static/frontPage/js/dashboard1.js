
$(function() {
    // ============================================================== 
    // Sales overview
    // ============================================================== 
    Morris.Area({
        element: 'earning',
        data: [{
                month: '2018-03-02',
                Cold: 300,
                Hot: 718,
            },{
                month: '2018-04-12',
                Cold: 310,
                Hot: 727,
            },{
                month: '2018-05-17',
                Cold: 320,
                Hot: 730,
            },{
                month: '2018-06-01',
                Cold: 330,
                Hot: 735,
            },{
                month: '2018-07-30',
                Cold: 340,
                Hot: 740,
            },{
                month: '2018-08-06',
                Cold: 347,
                Hot: 746,
            },{
                month: '2018-09-11',
                Cold: 354,
                Hot: 751,
            },{
                month: '2018-10-02',
                Cold: 360,
                Hot: 758,
            },
        ],
        xkey: 'month',
        ykeys: ['Cold', 'Hot'],
        labels: ['Cold', 'Hot'],
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
        xLabels: 'day',
        xLabelFormat: function (d) {
            var weekdays = new Array(7);
            weekdays[0] = "SUN";
            weekdays[1] = "MON";
            weekdays[2] = "TUE";
            weekdays[3] = "WED";
            weekdays[4] = "THU";
            weekdays[5] = "FRI";
            weekdays[6] = "SAT";

            return weekdays[d.getDay()] + '-' + 
                   ("0" + (d.getMonth() + 1)).slice(-2) + '-' + 
                   ("0" + (d.getDate())).slice(-2);
        },
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
            height: '5',
            resize: true,
            sliceColors: ['#1cadbf', '#1f5f67', '#ffffff']
        });
    }
    var sparkResize;

    sparklineLogin();


});