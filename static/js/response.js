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

function updateChart(tipe, iditem) {

    var tanggaldata = [];
    var valuedata = [];
    var mavaluedata = [];

    if(tipe == 'tanggal'){
        tanggaldata = tanggal[iditem];
        valuedata = valuetanggal[iditem];
        mavaluedata = mavaluetanggal[iditem];
    }else if(tipe == 'bulan'){
        tanggaldata = month[iditem];
        valuedata = valuemonth[iditem];
        mavaluedata = mavaluemonth[iditem];
    }else{
        tanggaldata = year[iditem];
        valuedata = valueyear[iditem];
        mavaluedata = mavalueyear[iditem];
    }

    listchart[iditem].data.datasets[0].data = valuedata;
    listchart[iditem].data.datasets[1].data = mavaluedata;
    listchart[iditem].data.labels = tanggaldata;
    listchart[iditem].update();
}

function addmainchart(idx, idelement){

    var ctx = document.getElementById(idelement);
    var idchart = new Chart($(ctx), {
      type: 'line',
      data: {
        labels: month[idx],
        datasets: [{
          backgroundColor: hexToRgba(getStyle('--info'), 10),
          borderColor: getStyle('--info'),
          pointHoverBackgroundColor: '#fff',
          borderWidth: 2,
          data: valuemonth[idx]
        }, {
          backgroundColor: hexToRgba(getStyle('--info'), 10),
          borderColor: '#FF0000',
          pointHoverBackgroundColor: '#fff',
          borderWidth: 2,
          data: mavaluemonth[idx]
        }]
      },
      options: {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              drawOnChartArea: false
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              maxTicksLimit: 5,
            }
          }]
        },
        elements: {
          point: {
            radius: 0,
            hitRadius: 10,
            hoverRadius: 4,
            hoverBorderWidth: 3
          }
        },
        plugins: {
            zoom: {
                // Container for pan options
                pan: {
                    // Boolean to enable panning
                    enabled: true,

                    // Panning directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow panning in the y direction
                    mode: 'xy'
                },

                // Container for zoom options
                zoom: {
                    // Boolean to enable zooming
                    enabled: true,

                    // Zooming directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow zooming in the y direction
                    mode: 'xy',
                }
            }
        }
      }
    });

    listchart.push(idchart);
}

var tanggalproduk = [];
var valueproduk= [];

function addlistchart(item, y){
    var ctx = document.getElementById(item);
    new Chart($(ctx), {
      type: 'line',
      data: {
        labels: tanggalproduk[y],
        datasets: [{
          backgroundColor: hexToRgba(getStyle('--info'), 10),
          borderColor: getStyle('--info'),
          pointHoverBackgroundColor: '#fff',
          borderWidth: 2,
          data: valueproduk[y]
        }]
      },
      options: {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              drawOnChartArea: false
            },
            ticks: {
                display: false
            }
          }],
          yAxes: [{
            ticks: {
                beginAtZero: true,
                maxTicksLimit: 5,
                max: 150
            }
          }]
        },
        elements: {
          point: {
            radius: 0,
            hitRadius: 10,
            hoverRadius: 4,
            hoverBorderWidth: 3
          }
        },
        plugins: {
            zoom: {
                // Container for pan options
                pan: {
                    // Boolean to enable panning
                    enabled: true,

                    // Panning directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow panning in the y direction
                    mode: 'xy'
                },

                // Container for zoom options
                zoom: {
                    // Boolean to enable zooming
                    enabled: true,

                    // Zooming directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow zooming in the y direction
                    mode: 'xy',
                }
            }
        }
      }
    });
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
                                    '<!-- <div id="totalterjual" class="small text-muted">Total Terjual' + data.terjual  +'Produk</div> -->' +
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
                                '<div class="chart-wrapper" style="height:300px;margin-top:40px;" id="containerchart">' +
                                    '<canvas class="chart" id="'+ data.judul +'"></canvas>' +
                                '</div>' +
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

                var total = 0;

                var produk = [];
                var jumlah = [];

                $.each(data.produk, function (i, item) {
                    var tempvalue = [];
                    var temptanggal = [];

                    $.each(item.DataTanggal, function (j, order) {
                        temptanggal.push(order.tanggal);
                        tempvalue.push(order.value);
                    });

                    tanggalproduk.push(temptanggal);
                    valueproduk.push(tempvalue);
                    produk.push(item.Produk);
                    jumlah.push(item.Jumlah);
                });

                $.each(jumlah, function (i, item) {
                    total += item;
                });

                var x=1;

                for(var i=0; i<produk.length; i++){
                    var percent = jumlah[i] / total * 100;

                    var canvastemplate = "" +
                        '<div class="chart-wrapper" style="height:130px;">' +
                            '<canvas class="chart" id="'+ produk[i] +'"></canvas>' +
                        '</div>';
                    var listvaluetemplate = "" +
                        '<div class="progress-group" style="margin-top: 2%;">' +
                          '<div class="progress-group-header align-items-end">' +
                            '<a data-toggle="modal" data-target="#exampleModalCenter" style="text-transform:capitalize;">' + x + '. ' + produk[i] + '</a>' +
                            '<div class="ml-auto font-weight-bold mr-2">' + jumlah[i] + '</div>' +
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
                    addlistchart(produk[i], i);
                    x++;
                }

                $("#produktinggi").text(data.produktinggi.nama);
                $("#valuetinggi").text(data.produktinggi.jumlah);
                $("#produktinggi3").text(data.last3month.nama);
                $("#valuetinggi3").text(data.last3month.jumlah);
                $("#produktinggi1").text(data.lastmonth.nama);
                $("#valuetinggi1").text(data.lastmonth.jumlah);
                $("#produkrendah").text(data.produkrendah.nama);
                $("#valuerendah").text(data.produkrendah.jumlah);

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
               }, 2000);
           }
       },
       error: function (data) {
           console.log("Error");
           homepage('Error saat proses pencarian, coba kembali');
       }
   });
});