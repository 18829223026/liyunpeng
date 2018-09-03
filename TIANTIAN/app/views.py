from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from .models import User, Category, Goods, Cart, CartGoods,Userinfo,OrderGoods,OrderInfo
from django.core.paginator import Paginator
import math


def index(request):
    """首页"""
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'categories': categories,
        'user': request.session.get('user')
    })


def goods_list(request):
    gjz = request.GET.get('q')
    if gjz != None:
        try:
            goods = Goods.objects.filter(name__icontains=gjz)
        except Exception:
            return HttpResponse('不存在该商品')
        paginator = Paginator(goods, 2)
        # 4. 获取页码
        num = request.GET.get('num', 1)
        # 5. 通过页码初始化当前页面的Page对象
        page = paginator.page(num)

        # 6. 返回响应结果
        return render(request, 'list.html', {
            'page': page,
            'goods':goods,
            'user': request.session.get('user'),
            'q': gjz
        })

    # 1. 获取分类ID
    category_id = request.GET.get('category_id')
    # 2. 根据分类ID查询该分类下面的所有商品
    try:
        goods = Category.objects.get(pk=category_id).goods_set.all()

    except Exception:
        return HttpResponse('不存在商品')
    # 3. 初始化Paginator分页类的对象
    paginator = Paginator(goods, 2)
    # 4. 获取页码
    num = request.GET.get('num', 1)
    # 5. 通过页码初始化当前页面的Page对象
    page = paginator.page(num)
    # 6. 返回响应结果
    return render(request, 'list.html', {
        'page': page,
        'category_id': category_id,
        'user': request.session.get('user'),

    })


def detail(request):
    goods_id = request.GET.get('goods_id')
    good = Goods.objects.get(pk=goods_id)

    return render(request, 'detail.html', {'goods': good,
                                           'user': request.session.get('user')})

# def detail(request, goods_id):
#     try:
#         goods = Goods.objects.get(pk=goods_id)
#         cart_goods_count = Cart.objects.get(user__username=request.session.get('user')).cartgoods_set.all().count()
#     except Exception:
#         return HttpResponse('不存在该商品')
#     print(cart_goods_count)
#     return render(request, 'detail.html', {'goods': goods, 'cart_goods_count': cart_goods_count})


def cart(request):
    cart = Cart.objects.get(user__username=request.session.get('user')).cartgoods_set.all()
    num = cart.count()
    return render(request, 'cart.html', {'car': cart,
                                         'num': num,
                                         'user': request.session.get('user')})


def add_to_cart(request):
    # 获取请求提交的商品id和数量
    goods_id = request.POST.get('goods_id')
    number = request.POST.get('number')
    try:
        # get_or_create 返回 (object, created) object是数据对象，
        # created为布尔值，true为创建的数据，false为查询的数据
        # 获取当前用户的购物车
        cart = Cart.objects.get_or_create(
            user__username=request.session.get('user'),
            defaults={
                'user_id': User.objects.get(username=request.session.get('user')).id
            }
        )
    except Exception:
        return HttpResponse('没有该用户')
    # 给当前用户的购物车添加或更新商品数量
    cartgoods = CartGoods.objects.update_or_create(cart=cart[0], goods_id=goods_id)

    cartgoods[0].number += int(number)
    cartgoods[0].save()
    # 返回结果
    if cartgoods[0]:
        return HttpResponse(cart[0].cartgoods_set.count())
    else:
        return HttpResponse('添加失败')




def order(request):
    import json
    # 获取到被选中到商品的ID们
    cartgoods = json.loads(request.GET.get('data'))
    ids = []
    for item in cartgoods:
        ids.append(item['cartgoods_id'])
        CartGoods.objects.filter(pk=item['cartgoods_id']).update(number=item['number'])
    data = CartGoods.objects.filter(id__in=ids)
    return render(request,'place_order.html',{'cartgoods':data,
                                              'user': request.session.get('user')})

# def goods_list(request):
#     """商品列表页面"""
#     # 获取get请求传递低参数
#     category_id = request.GET.get('category_id')
#     # 从页面获取当前点击的页码（转成整数类型）
#     page = int(request.GET.get('page', 1))
#     is_first = True
#     if page != 1:
#         is_first = False
#     # 获取当前分类下的所有商品
#     goods = Category.objects.get(pk=category_id).goods_set.all()
#     # 计算总页码
#     pages = range(1, math.ceil(goods.count() / 1) + 1)
#     return render(request, 'list.html', {
#         'category_id': category_id,
#         'goods': goods[(page-1)*1:(page-1)*1+1],
#         'pages': pages,
#         'is_first': is_first
#     })


def register(request):
    """用户注册处理"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create(
                username=data['username'],
                password=data['password'],
                email=data['email'],
            )
            if user is not None:
                return render(request,'index.html')
            else:
                return HttpResponse('注册失败')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    """用户登录处理"""
    if request.method == 'POST':
        # 用表单提交过来的数据创建一个LoginForm对象
        form = LoginForm(request.POST)
        # 判断表单数据是否合法
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.get(
                    username=data['username'],
                    password=data['password']
                )
            except Exception:
                return HttpResponse('用户名密码错误')
            # 登录成功, 需要将当前登录的用户保存记录下来
            # 使用session存储数据，可以在服务端进行全局共享
            request.session['user'] = user.serializable_value('username')
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def center_info(request):
    user_id = User.objects.get(username=request.session.get('user')).id
    add = Userinfo.objects.filter(user_id=user_id,id=1)
    return render(request,'user_center_info.html',{'add':add,
                                                   'user':request.session.get('user')})


def center_order(request):
    user_id = User.objects.get(username=request.session.get('user')).id
    dingdans = OrderInfo.objects.filter(user_id=user_id)
    paginator = Paginator(dingdans, 1)
    # 4. 获取页码
    num = request.GET.get('num', 1)
    # 5. 通过页码初始化当前页面的Page对象
    page = paginator.page(num)
    # 6. 返回响应结果
    price = OrderGoods.objects.filter(order_info__user_id=user_id).all()
    a = 0
    for i in price:
        a += i.goods.price * i.number

    return render(request, 'user_center_order.html', {
        'page': page,
        'user': request.session.get('user'),
        'a':a,
    })

def center_site(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        user_id = User.objects.get(username=request.session.get('user')).id
        user = Userinfo.objects.create(
            recipient=recipient,address=address,postcode=postcode,phone=phone,user_id=user_id
        )
        if user is not None:
            return render(request,'user_center_site.html')
        else:
            return HttpResponse('提交失败')

    return render(request,'user_center_site.html',{'user':request.session.get('user')})


def add(request):
    #添加订单商品到数据库
    user_id = User.objects.get(username=request.session.get('user')).id
    ordergoods_id = request.POST.get('ordergoods_id')
    aa = ordergoods_id.strip().split(',')
    print(aa)
    cartgoods = CartGoods.objects.filter(id__in=aa)
    print(cartgoods)
    order = OrderInfo.objects.create(user_id=user_id,pay_status=0,shipping_status=0)
    for i in cartgoods:
        ordergoods = OrderGoods.objects.create(
            order_info=order,goods=i.goods,number=i.number
        )
    if ordergoods:
        #点击删除按钮同步删除数据库商品
        CartGoods.objects.filter(id__in=aa).delete()
    return render(request,'user_center_order.html')


def delete(request):
    cart_goods_id=request.GET.get('cart_goods_id')
    goods_id = CartGoods.objects.filter(id=cart_goods_id).delete()
    return redirect('cart')

