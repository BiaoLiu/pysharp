from django.http import HttpResponse
from django.shortcuts import render
from stock.tasks import add, add2


# Create your views here.

def testadd1(request):
    a = request.GET.get('a', 1)
    b = request.GET.get('b', 1)

    r = add.delay(int(a), int(b))
    # print(r.id)

    return HttpResponse('success:'+r.id)
