var tanggal = [];
var month = [];
var year = [];
var valuetanggal = [];
var valuemonth = [];
var valueyear = [];

var tanggalproduk = [];
var valueproduk = [];

function yearChart() {
  mainChart.data.datasets[0].data =valueyear;
  mainChart.data.labels = year;
  mainChart.update();
}

function monthChart() {
  mainChart.data.datasets[0].data = valuemonth;
  mainChart.data.labels = month;
  mainChart.update();
}

function dayChart() {
  mainChart.data.datasets[0].data =valuetanggal;
  mainChart.data.labels = tanggal;
  mainChart.update();
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
        }
      }
    });
}

var statebag = 0;
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
                if(data.result == "Bag of Word" && statebag == 0){
                    $.each(data.day, function (i, item) {
                        tanggal.push(item.tanggal);
                        valuetanggal.push(item.value);
                    });

                    $.each(data.month, function (i, item) {
                        month.push(item.tanggal);
                        valuemonth.push(item.value);
                    });

                    $.each(data.year, function (i, item) {
                        year.push(item.tanggal);
                        valueyear.push(item.value);
                    });
                    monthChart();
                    $("#tinggihari").text(data.tinggihari.tanggal + " (" + data.tinggihari.value + ")");
                    $("#tinggibulan").text(data.tinggibulan.tanggal + " (" + data.tinggibulan.value + ")");
                    $("#tinggitahun").text(data.tinggitahun.tanggal + " (" + data.tinggitahun.value + ")");
                    $("#rendahhari").text(data.rendahhari.tanggal + " (" + data.rendahhari.value + ")");
                    $("#rendahbulan").text(data.rendahbulan.tanggal + " (" + data.rendahbulan.value + ")");
                    $("#rendahtahun").text(data.rendahtahun.tanggal + " (" + data.rendahtahun.value + ")");
                    statebag = 1;
                }
                else if(data.result == "Produk Tertinggi dan Terendah"){
                    $("#produktinggi").text(data.produktinggi.nama);
                    $("#valuetinggi").text(data.produktinggi.jumlah);
                    $("#produktinggi3").text(data.produk3month.nama);
                    $("#valuetinggi3").text(data.produk3month.jumlah);
                    $("#produktinggi1").text(data.produkmonth.nama);
                    $("#valuetinggi1").text(data.produkmonth.jumlah);
                    $("#produkrendah").text(data.produkrendah.nama);
                    $("#valuerendah").text(data.produkrendah.jumlah);
                }
                else if(data.result == "Jumlah dan Tanggal Produk"){
                    $.each(data.listproduk, function (i, item) {
                        var tempvalue = [];
                        var temptanggal = [];

                        $.each(item, function (j, order) {
                            temptanggal.push(order.tanggal);
                            tempvalue.push(order.value);
                        });

                        tanggalproduk.push(temptanggal);
                        valueproduk.push(tempvalue);
                    });
                }
           }else{
                var total = 0;
                $.each(data.result, function (i, item) {
                    total += item.Jumlah;
                });
                $("#totalulasan").text("Total Terjual " + total + " Produk");
                var x=1,y=0;
                $.each(data.result, function (i, item) {
                    var percent = item.Jumlah / total * 100;

                    var canvastemplate = "" +
                        '<div class="chart-wrapper" style="height:130px;">' +
                            '<canvas class="chart" id="'+ item.Produk +'"></canvas>' +
                        '</div>';
                    var listvaluetemplate = "" +
                        '<div class="progress-group" style="margin-top: 2%;">' +
                          '<div class="progress-group-header align-items-end">' +
                            '<a href="#" data-toggle="modal" data-target="#exampleModalCenter" style="text-transform:capitalize;">' + x + '. ' + item.Produk + '</a>' +
                            '<div class="ml-auto font-weight-bold mr-2">' + item.Jumlah + '</div>' +
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
                    addlistchart(item.Produk, y);
                    x++;
                    y++;
                });

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
       }
   });
});