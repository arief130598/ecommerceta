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

        if task.state == "PROGRESS" or task.state == "PENDING":
            data = {
                'state': task.state,
                'result': task.result
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {
                'state': task.state,
                'result': json.loads(task.result)
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')


def search(request):
    idtask = 0
    katmodel = ''
    katmodel2 = ''

    box1 = request.POST.get('box1')
    box2 = request.POST.get('box2')
    box3 = request.POST.get('box3')

    if box1 == "men":
        if box2 == 'Clothing':
            print(box2)
        elif box2 == 'Shoes':
            if box3 == '':
                k = 8
                katmodel = 'Sepatu Pria'
                task = totalulasan.delay(k, katmodel, katmodel2)
                idtask = task.id
        else:
            print(box2)

    if katmodel2 == '':
        kategori = box1 + " > " + box2
        title = katmodel
    else:
        title = katmodel2
        kategori = box1 + " > " + box2 + " > " + box3

    list_variabel = {
        'title': title,
        'kategori': kategori,
        'task_id': idtask
    }

    if idtask is not 0:
        return render(request, 'ecommercetrends/search.html', list_variabel)
    else:
        return render(request, 'ecommercetrends/search.html')
