from django.shortcuts import render

# Create your views here.
from ecommercetrends.tasks import totalulasan


def home(request):
    return render(request, 'home.html')


def search(request):
    idtask = 0

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
                katmodel2 = ''
                task = totalulasan.delay(k, katmodel, katmodel2)
                idtask = task.id
        else:
            print(box2)

    if idtask is not 0:
        return render(request, 'ecommercetrends/search.html', {'task_id': idtask})
    else:
        return render(request, 'ecommercetrends/search.html')