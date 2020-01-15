import json

from celery.result import AsyncResult
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ecommercetrends.tasks import tasksearch


def home(request):
    return render(request, 'home.html')


def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        if task.state == "PENDING":
            data = {
                'state': task.state,
                'result': task.result
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif task.state == "PROGRESS":
            if task.info.get('status') == "Bag of Word":
                data = {
                    'state': task.state,
                    'result': task.info.get('status'),
                    'day': json.loads(task.info.get('day')),
                    'month': json.loads(task.info.get('month')),
                    'year': json.loads(task.info.get('year')),
                    'tinggihari': json.loads(task.info.get('tinggihari')),
                    'tinggibulan': json.loads(task.info.get('tinggibulan')),
                    'tinggitahun': json.loads(task.info.get('tinggitahun')),
                    'rendahhari': json.loads(task.info.get('rendahhari')),
                    'rendahbulan': json.loads(task.info.get('rendahbulan')),
                    'rendahtahun': json.loads(task.info.get('rendahtahun')),
                    'judul': task.info.get('judul'),
                    'maday': json.loads(task.info.get('maday')),
                    'mamonth': json.loads(task.info.get('mamonth')),
                    'mayear': json.loads(task.info.get('mayear')),
                    'jumlahterjual': task.info.get('jumlahterjual'),
                    'jumlahulasan': task.info.get('jumlahulasan')
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = {
                    'state': task.state,
                    'result': task.info.get('status')
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
        elif task.state == 'SUCCESS':
            if task.result == 'FAIL':
                data = {
                    'status': 'FAIL',
                    'response': 'Dari keyword yang dicari data tidak ditemukan'
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

            dataproduk = json.loads(task.result.get('dataproduk'))
            dataproduk = [json.loads(i) for i in dataproduk]
            datamaproduk = json.loads(task.result.get('datamaproduk'))
            datamaproduk = [json.loads(i) for i in datamaproduk]

            data = {
                'state': task.state,
                'namaproduk': json.loads(task.result.get('namaproduk')),
                'dataproduk': dataproduk,
                'datamaproduk': datamaproduk,
                'jumlahterjual': json.loads(task.result.get('jumlahterjual')),
                'jumlahulasan': json.loads(task.result.get('jumlahulasan')),
                'jumlahulasan3bulan': json.loads(task.result.get('jumlahulasan3bulan')),
                'jumlahulasan1bulan': json.loads(task.result.get('jumlahulasan1bulan')),
                'tertinggi': json.loads(task.result.get('tertinggi')),
                'terendah': json.loads(task.result.get('terendah')),
                'terakhir3': json.loads(task.result.get('terakhir3')),
                'terakhir1': json.loads(task.result.get('terakhir1')),
                'yaxis': int(task.result.get('yaxis'))
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {
                'state': task.state,
                'result': task.result
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')


def search(request):
    idtask = 0

    ecommerce = request.POST.get('ecommerce')
    datestart = request.POST.get('datestart')
    dateend = request.POST.get('dateend')
    kategori = request.POST.get('kategoriutama')
    keyword = request.POST.get('searchkeyword')

    task = tasksearch.delay(ecommerce, datestart, dateend, kategori, keyword)
    idtask = task.id

    if idtask is not 0:
        return render(request, 'ecommercetrends/search.html', {'task_id': idtask})
    else:
        return render(request, 'ecommercetrends/search.html')
