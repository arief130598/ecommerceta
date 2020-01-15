var tanggal = [];
var month = [];
var year = [];
var valuetanggal = [];
var valuemonth = [];
var valueyear = [];

var mavaluetanggal = [];
var mavaluemonth = [];
var mavalueyear = [];

var listchart = [];
var yaxis;

function updateChart(tipe, iditem) {
    chartdatatemp = [];

    if(tipe == 'tanggal'){
        for(var j=0; j<tanggal[iditem].length; j++){
            chartdatatemp.push({
               label: tanggal[iditem][j],
               value: valuetanggal[iditem][j],
               valuema: mavaluetanggal[iditem][j]
            });
        }
    }else if(tipe == 'bulan'){
        for(var i=0; i<month[iditem].length; i++){
            chartdatatemp.push({
               label: month[iditem][i],
               value: valuemonth[iditem][i],
               valuema: mavaluemonth[iditem][i]
            });
        }
    }else{
        for(var k=0; k<year[iditem].length; k++){
            chartdatatemp.push({
               label: year[iditem][k].toString(),
               value: valueyear[iditem][k],
               valuema: mavalueyear[iditem][k]
            });
        }
        console.log(chartdatatemp);
    }

    listchart[iditem].data = chartdatatemp;
    listchart[iditem].invalidateData();
}

function addmainchart(idx, idelement){

    var chartmain = am4core.create(idelement, am4charts.XYChart);

    chartdatatemp = [];
    for(var i=0; i<month[idx].length; i++){
        chartdatatemp.push({
           label: month[idx][i].toString(),
           value: valuemonth[idx][i],
           valuema: mavaluemonth[idx][i]
        });
    }

    chartmain.data = chartdatatemp;

    // Create axes
    var dateAxis = chartmain.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;
    dateAxis.renderer.grid.template.disabled = true;

    var valueAxis = chartmain.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = chartmain.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "label";
    series.stroke = am4core.color("#0000ff");
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 0.5;
    series.tooltip.label.padding(12,12,12,12);
    series.tensionX = 0.77;

    // Create series
    var series2 = chartmain.series.push(new am4charts.LineSeries());
    series2.dataFields.valueY = "valuema";
    series2.dataFields.dateX = "label";
    series2.stroke = am4core.color("#ff0000");
    series2.strokeWidth = 2;
    series2.minBulletDistance = 10;
    series2.tooltipText = "{valueY}";
    series2.tooltip.pointerOrientation = "vertical";
    series2.tooltip.background.cornerRadius = 20;
    series2.tooltip.background.fillOpacity = 0.5;
    series2.tooltip.label.padding(12,12,12,12);
    series2.tensionX = 0.77;

    // Add scrollbar
    chartmain.scrollbarX = new am4charts.XYChartScrollbar();
    chartmain.scrollbarX.series.push(series);

    // Add cursor
    chartmain.cursor = new am4charts.XYCursor();
    chartmain.cursor.xAxis = dateAxis;
    chartmain.cursor.snapToSeries = series;

    listchart.push(chartmain);
}

var tanggalproduk = [];
var valueproduk= [];
var valueprodukma = [];

function addlistchart(item, y){

    var chart = am4core.create(item, am4charts.XYChart);

    chartdatatemp = [];
    for(var i=0; i<tanggalproduk[y].length; i++){
        chartdatatemp.push({
           label: tanggalproduk[y][i],
           value: valueproduk[y][i],
           valuema: valueprodukma[y][i]
        });
    }

    chart.data = chartdatatemp;

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;
    dateAxis.renderer.grid.template.disabled = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.max = yaxis;

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "label";
    series.stroke = am4core.color("#0000ff");
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 0.5;
    series.tooltip.label.padding(12,12,12,12);
    series.tensionX = 0.77;

    // Create series
    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.valueY = "valuema";
    series2.dataFields.dateX = "label";
    series2.stroke = am4core.color("#ff0000");
    series2.strokeWidth = 2;
    series2.minBulletDistance = 10;
    series2.tooltipText = "{valueY}";
    series2.tooltip.pointerOrientation = "vertical";
    series2.tooltip.background.cornerRadius = 20;
    series2.tooltip.background.fillOpacity = 0.5;
    series2.tooltip.label.padding(12,12,12,12);
    series2.tensionX = 0.77;

    // Add scrollbar
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series);

    // Add cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.cursor.snapToSeries = series;
}

var iproduk = 0;
var judultemp = '';

function homepage(status){
    alert(status);
    window.location = "http://127.0.0.1:8000";
}

$(function get_task() {
    $.ajax({
       url: url,
       data:{'task_id': id},
       type:'get',
       success: function (data) {
           if (data.state == 'PENDING') {
                console.log('Please wait...');
           }
           else if (data.state == 'PROGRESS') {
                console.log(data.result);
                $("#statusloading").text(data.result);
                if(data.result == "Bag of Word"){
                    if(judultemp != data.judul){
                        judultemp = data.judul;
                        console.log(judultemp);

                        var tanggaltemp = [];
                        var bulantemp = [];
                        var tahuntemp = [];

                        var itemtanggaltemp = [];
                        var itembulantemp = [];
                        var itemtahuntemp = [];

                        var maitemtanggaltemp = [];
                        var maitembulantemp = [];
                        var maitemtahuntemp = [];

                        $.each(data.day, function (i, item) {
                            tanggaltemp.push(item.tanggal);
                            itemtanggaltemp.push(item.value);
                        });

                        $.each(data.month, function (i, item) {
                            bulantemp.push(item.tanggal);
                            itembulantemp.push(item.value);
                        });

                        $.each(data.year, function (i, item) {
                            tahuntemp.push(item.tanggal);
                            itemtahuntemp.push(item.value);
                        });

                        $.each(data.maday, function (i, item) {
                            maitemtanggaltemp.push(item.value);
                        });

                        $.each(data.mamonth, function (i, item) {
                            maitembulantemp.push(item.value);
                        });

                        $.each(data.mayear, function (i, item) {
                            maitemtahuntemp.push(item.value);
                        });

                        tanggal.push(tanggaltemp);
                        month.push(bulantemp);
                        year.push(tahuntemp);
                        valuetanggal.push(itemtanggaltemp);
                        valuemonth.push(itembulantemp);
                        valueyear.push(itemtahuntemp);
                        mavaluetanggal.push(maitemtanggaltemp);
                        mavaluemonth.push(maitembulantemp);
                        mavalueyear.push(maitemtahuntemp);
                        tgl = 'tanggal';
                        bln = 'bulan';
                        yr = 'tahun';

                        var maincharttemplate = '' +
                              '<div class="card-body">' +
                                '<div class="row">' +
                                  '<div class="col-sm-5">' +
                                   '<h4 class="card-title mb-0" style="text-transform:capitalize;">' + data.judul +'</h4>' +
                                    '<div id="totalterjual" class="small text-muted">Total Terjual ' + data.jumlahterjual  +' Produk</div>' +
                                    '<div id="totalterjual" class="small text-muted">Total Ulasan ' + data.jumlahulasan  +' Ulasan</div>' +
                                  '</div>' +
                                  '<!-- /.col-->' +
                                 '<div class="col-sm-7 d-none d-md-block">' +
                                    '<div class="btn-group btn-group-toggle float-right mr-3" data-toggle="buttons">' +
                                      '<label class="btn btn-outline-secondary" onclick="updateChart(\'' + tgl +'\',' + iproduk + ')">' +
                                        '<input id="option1" type="radio" name="options" autocomplete="off"> Day' +
                                      '</label>' +
                                      '<label class="btn btn-outline-secondary active" onclick="updateChart(\'' + bln +'\',' + iproduk + ')">' +
                                        '<input id="option2" type="radio" name="options" autocomplete="off"> Month' +
                                      '</label>' +
                                      '<label class="btn btn-outline-secondary"  onclick="updateChart(\'' + yr +'\',' + iproduk + ')">' +
                                        '<input id="option3" type="radio" name="options" autocomplete="off"> Year' +
                                      '</label>' +
                                    '</div>' +
                                  '</div>' +
                                  '<!-- /.col-->' +
                                '</div>' +
                                '<!-- /.row-->' +
                                '<!--Line Chart-->' +
                                '<div style="height:400px; width:100%;" id="' + data.judul + '"></div>' +
                                '<!--End of Line Chart-->' +
                              '</div>' +
                              '<div class="card-footer">' +
                                '<div class="row text-center">' +
                                  '<div class="col-sm-12 col-md mb-sm-2 mb-0">' +
                                    '<div class="text-muted">Penjualan Tertinggi (Hari)</div>' +
                                    '<strong id="tinggihari" >'+ data.tinggihari.tanggal + ' (' + data.tinggihari.value + ')' +'</strong>' +
                                  '</div>' +
                                  '<div class="col-sm-12 col-md mb-sm-2 mb-0">' +
                                      '<div class="text-muted">Penjualan Tertinggi (Bulan)</div>' +
                                      '<strong id="tinggibulan">'+ data.tinggibulan.tanggal + " (" + data.tinggibulan.value + ")" +'</strong>' +
                                  '</div>' +
                                  '<div class="col-sm-12 col-md mb-sm-2 mb-0">' +
                                    '<div class="text-muted">Penjualan Tertinggi (Tahun)</div>' +
                                    '<strong  id="tinggitahun">'+ data.tinggitahun.tanggal + " (" + data.tinggitahun.value + ")" +'</strong>' +
                                  '</div>' +
                                  '<div class="col-sm-12 col-md mb-sm-2 mb-0">' +
                                    '<div class="text-muted">Penjualan Terendah (Hari)</div>' +
                                    '<strong id="rendahhari">'+ data.rendahhari.tanggal + " (" + data.rendahhari.value + ")" +'</strong>' +
                                  '</div>' +
                                  '<div class="col-sm-12 col-md mb-sm-2 mb-0">' +
                                      '<div class="text-muted">Penjualan Terendah (Bulan)</div>' +
                                      '<strong id="rendahbulan">'+ data.rendahbulan.tanggal + " (" + data.rendahbulan.value + ")" +'</strong>' +
                                  '</div>' +
                                  '<div class="col-sm-12 col-md mb-sm-2 mb-0">' +
                                    '<div class="text-muted">Penjualan Terendah (Tahun)</div>' +
                                    '<strong id="rendahtahun">'+ data.rendahtahun.tanggal + " (" + data.rendahtahun.value + ")" +'</strong>' +
                                  '</div>' +
                                '</div>' +
                              '</div>';


                        $("#mainproduk").append(maincharttemplate);
                        addmainchart(iproduk, data.judul);
                        iproduk += 1;
                    }
                }
           }else{
                if(data.status == 'FAIL'){
                    homepage(data.response);
                }

                yaxis = data.yaxis;

                var total = 0;

                var namaproduk = [];
                var jumlahterjual = [];
                var jumlahulasan = [];

                $.each(data.namaproduk, function (i, item) {
                    namaproduk.push(item)
                });

                $.each(data.jumlahterjual, function (i, item) {
                    jumlahterjual.push(item)
                });

                $.each(data.jumlahulasan, function (i, item) {
                    jumlahulasan.push(item)
                });

                $.each(data.dataproduk, function (i, item) {
                    var tempvalue = [];
                    var temptanggal = [];

                    $.each(item, function (j, order) {
                        temptanggal.push(order.tanggal);
                        tempvalue.push(order.value);
                    });

                    tanggalproduk.push(temptanggal);
                    valueproduk.push(tempvalue);
                });

                $.each(data.datamaproduk, function (i, item) {
                    var tempvaluema = [];

                    $.each(item, function (j, order) {
                        tempvaluema.push(order.value);
                    });
                    valueprodukma.push(tempvaluema);
                });

                $.each(jumlahterjual, function (i, item) {
                    total += item;
                });

                var x=1;

                for(var i=0; i<namaproduk.length; i++){
                    var percent = jumlahterjual[i] / total * 100;

                    var canvastemplate = '<div style="height:250px; width:100%; margin-top: -5px;" id="' + namaproduk[i] + '"></div>';
                    var listvaluetemplate = "" +
                        '<div class="progress-group" style="margin-top: 2%;">' +
                          '<div class="progress-group-header align-items-end">' +
                            '<a data-toggle="modal" data-target="#exampleModalCenter" style="text-transform:capitalize;">' + x + '. ' + namaproduk[i] + '</a>' +
                            '<div class="ml-auto font-weight-bold mr-2"> Terjual : ' + jumlahterjual[i] + '   Ulasan : ' + jumlahulasan[i] + '</div>' +
                            '<div class="text-muted small">' + Math.round(percent * 100) / 100 + '%</div>' +
                          '</div>' +
                          '<div class="progress-group-bars">' +
                            '<div class="progress progress-xs">' +
                              '<div class="progress-bar" role="progressbar" style="width:' + Math.round(percent * 100) / 100 + '%" aria-valuenow="56" aria-valuemin="0" aria-valuemax="100"></div>' +
                            '</div>' +
                          '</div>' +
                        '</div>';

                    $("#listvalue").append(listvaluetemplate);
                    $("#listvalue").append(canvastemplate);
                    addlistchart(namaproduk[i], i);
                    x++;
                }

                $("#produktinggi").text(data.tertinggi.nama);
                $("#valuetinggi").text(data.tertinggi.jumlah);
                $("#produktinggi3").text(data.terakhir3.nama);
                $("#valuetinggi3").text(data.terakhir3.jumlah);
                $("#produktinggi1").text(data.terakhir1.nama);
                $("#valuetinggi1").text(data.terakhir1.jumlah);
                $("#produkrendah").text(data.terendah.nama);
                $("#valuerendah").text(data.terendah.jumlah);

                $("html").css({"background-color": "#e4e5e6", "overflow-x": "visible", "overflow-y": "visible",});
                $("body").css({"background-color": "#e4e5e6", "overflow-x": "visible", "overflow-y": "visible",});
                $("#loadingbar").fadeOut('slow');
                $("#header").fadeIn(2000)
                $("#main").fadeIn(2000);
                $("#footer").fadeIn(2000);
           }
           if(data.state != 'SUCCESS') {
               setTimeout(function () {
                   get_task()
               }, 3000);
           }
       },
       error: function (data) {
           console.log("Error");
           homepage('Error saat proses pencarian, coba kembali');
       }
   });
});