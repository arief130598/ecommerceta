var tanggal = [];
var month = [];
var year = [];
var valuetanggal = [];
var valuemonth = [];
var valueyear = [];

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
                    statebag = 1;
                }
           }else{
                var total = 0;
                $.each(data.result, function (i, item) {
                    total += item.Jumlah;
                });
                $("#totalulasan").text("Total Terjual " + total + " Produk");
                var x=1;
                $.each(data.result, function (i, item) {
                    var percent = item.Jumlah / total * 100;

                    var listvaluetemplate = "" +
                        '<div class="progress-group">' +
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
                    x++;
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