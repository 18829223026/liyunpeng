from django.shortcuts import render
from .models import Rshouche1,Luntan1
from django.db.models import Count,Avg,Max,Min
# Create your views here.
def xm(request):
    bb=set()
    car_name = Rshouche1.objects.all()
    aa = Rshouche1.objects.all().order_by('price').count()
    bb = Rshouche1.objects.all().aggregate(Avg('lucheng'),Max('price'),Min('price'))
    ddd = Rshouche1.objects.all().aggregate(Avg('price'))
    where_ = Rshouche1.objects.values('where_field').annotate(Count=Count('where_field')).order_by()
    ctx=post1(request)
    print(ctx)
    if ctx:
        return render(request, 'xm.html',{'car_name':car_name,'where_':where_,'aa':aa,'bb':bb,'ddd':ddd,'ctx':ctx})
    else:
        return render(request, 'xm.html', {'car_name': car_name, 'where_': where_, 'aa': aa, 'bb': bb, 'ddd': ddd})
def LT(request):
    aa = Luntan1.objects.order_by('-clinck')[:20]
    return render(request,'LT.html',{'aa':aa})

def post1(request):
    if request.method=='POST':
        rlt= request.POST['q']
        if rlt:
            ccc = Rshouche1.objects.filter(car_name__contains=rlt).values('price','lucheng','guige','url_field').order_by('price').first()
        else:
            ccc=None

    else:
        ccc=None


    return ccc


