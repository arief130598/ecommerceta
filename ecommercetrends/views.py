import json

from celery.result import AsyncResult
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ecommercetrends.tasks import totalulasan


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
                    'mayear': json.loads(task.info.get('mayear'))
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

            data = {
                'state': task.state,
                'produk': json.loads(task.result.get('produk')),
                'produktinggi': json.loads(task.result.get('produktinggi')),
                'produkrendah': json.loads(task.result.get('produkrendah')),
                'lastmonth': json.loads(task.result.get('lastmonth')),
                'last3month': json.loads(task.result.get('last3month')),
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
    katmodel2 = ''

    datestart = request.POST.get('datestart')
    dateend = request.POST.get('dateend')
    box1 = request.POST.get('box1')
    box2 = request.POST.get('box2')
    box3 = request.POST.get('searchkeyword')

    if box1 == "men":
        if box2 == 'Clothing':
            print(box2)
        elif box2 == 'Shoes':
            if box3 == '':
                katmodel = 'Sepatu Pria'
                task = totalulasan.delay(katmodel, katmodel2, datestart, dateend)
                idtask = task.id
            else:
                box3 = box3.lower()
                katmodel = 'Sepatu Pria'
                katmodel2 = box3
                task = totalulasan.delay(katmodel, katmodel2, datestart, dateend)
                idtask = task.id
        else:
            print(box2)


    if idtask is not 0:
        return render(request, 'ecommercetrends/search.html', {'task_id': idtask})
    else:
        return render(request, 'ecommercetrends/search.html')
