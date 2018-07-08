from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from .models import *
import hashlib, uuid, os
from AXF.settings import *


# ******************************基础页面显示***********************************
# 首页
def home(request):
    # 轮播数据
    wheels = HomeWheel.objects.all()
    # 导航数据
    navs = HomeNav.objects.all()
    # 必购
    mustbuys = HomeMustBuy.objects.all()
    # shop
    shops = HomeShop.objects.all()
    shop0 = shops.first()
    shop1_2 = shops[1:3]
    shop3_6 = shops[3:7]
    shop7_10 = shops[7:11]
    # 主要商品
    mainshows = HomeShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop1_2': shop1_2,
        'shop3_6': shop3_6,
        'shop7_10': shop7_10,
        'mainshows': mainshows
    }

    return render(request, 'home/home.html', data)


# 闪购
def market(request):
    return redirect(reverse('axf:marketwithparams', args=['104749', '0', '0']))


# 闪购分类
def market_with_params(request, typeid, childid, sortid):
    # 主分类数据
    foodtypes = FoodType.objects.all()
    # 所有商品数据
    goods_list = Goods.objects.filter(categoryid=typeid)

    # 子分类下数据
    if childid != '0':
        goods_list = goods_list.filter(childcid=childid)

    # 获取当前主分类下的子分类
    main_type = foodtypes.get(typeid=typeid)
    childtypenames = main_type.childtypenames
    # print(childtypenames)
    # 全部分类: 0  # 进口水果:103534#国产水果:103533

    child_type_list = childtypenames.split("#")

    child_types = []  #
    for type in child_type_list:
        # print(type) #全部分类:0
        type_list = type.split(":")
        # print(type_list) #['全部分类', '0']
        child_types.append(type_list)
        # print(child_types)#[['全部分类', '0'], ['进口水果', '103534'], ['国产水果', '103533']]

    # 排序
    # 综合排序
    if sortid == '0':
        goods_list = goods_list.order_by('-productnum')
    # 销量排序
    elif sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    # 价格降序
    elif sortid == '2':
        goods_list = goods_list.order_by('-price')
    # 价格升序
    elif sortid == '3':
        goods_list = goods_list.order_by('price')

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': typeid,
        'child_types': child_types,
        'childid': childid,
    }
    return render(request, 'market/market.html', data)


# 我的
def mine(request):
    # 獲取session
    userid = request.session.get('userid', 0)

    user = User.objects.filter(id=userid)
    data = {
        'name': '',
        'icon': '',
    }

    if user.exists():
        data['name'] = user.first().name
        data['icon'] = user.first().icon

    return render(request, 'mine/mine.html', data)


# ******************************注册功能***********************************
# 注册
def register(request):
    return render(request, 'user/register.html')


# 注册请求处理
def register_handle(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        icon = request.FILES.get('file')

        # 服务器端做注册信息验证
        # if len(username) < 6:
        #     data = {
        #         'status': 1,
        #         'msg': "用户长度不够"
        #     }
        #     return render(request,'user/register.html',data)

        # 注册信息加入数据库表中
        user = User()
        user.name = username
        user.passwd = password  # my_md5(password),还可以使用register.js中md5加密
        user.email = email

        if icon:

            # 图片名称
            icon_name = generate_iconname() + '.png'

            # 图片数据路径存入本地
            user.icon = '/uploads/icon/' + icon_name

            # 图片存入本地
            file_path = os.path.join(MEDIA_ROOT, icon_name)
            with open(file_path, 'ab') as fp:
                for part in icon.chunks():
                    fp.write(part)
                    fp.flush()

        user.save()

        # 注册后自动登录
        # 保存session
        request.session['userid'] = user.id
        # 自动跳转到‘我的’页面
        return redirect(reverse('axf:mine'))
    else:
        return redirect(reverse('axf:register'))


# 輔助函數 - md5加密
def my_md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


# 輔助函數-生成随机名称
def generate_iconname():
    u = str(uuid.uuid4())
    return my_md5(u)


# 验证用户是否存在
def check_username(request):
    # ajax请求
    if request.method == 'GET':
        username = request.GET.get('username')

        users = User.objects.filter(name=username)
        if users.exists():
            return JsonResponse({'status': 0, 'msg': '用户名已存在'})
        else:
            return JsonResponse({'status': 1, 'msg': '用户名可用'})

    else:
        return JsonResponse({'status': -1, 'msg': "请求方式错误"})


# ******************************登录功能***********************************
# 退出登录
def logout(request):
    # 清除session
    del request.session['userid']
    request.session.flush()

    return redirect(reverse('axf:mine'))


# 登录
def login(request):
    return render(request, 'user/login.html')


# 登录请求处理
def login_handle(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 登录:匹配用户名密码
        users = User.objects.filter(name=username, passwd=password)

        if users.exists():
            # 登录成功
            # session
            request.session['userid'] = users.first().id

            return redirect(reverse('axf:mine'))

        else:
            # 登录失败
            data = {
                'status': 0,
                'msg': "用户名或密码错误", }

            return render(request, 'user/login.html', data)
    else:
        data = {
            'status': -1,
            'msg': "请求方式错误", }
        return render(request, 'user/login.html', data)


# ******************************购物车功能***********************************
# 购物车
def cart(request):
    # 获取当前登录用户购物车所有数据
    userid = request.session.get('userid', 0)  # session获取当前登录用户
    if not userid:
        return redirect(reverse('axf:login'))

    carts = Cart.objects.filter(user_id=userid)
    data = {
        'carts': carts,
    }
    return render(request, 'cart/cart.html', data)


# 加入购物车
def cart_add(request):
    data = {
        'status': 1,
        'msg': 'ok'
    }
    userid = request.session.get('userid')
    if not userid:
        # 未登录
        data['status'] = 0
        data['msg'] = '未登录'
        return JsonResponse(data)
    else:
        # 已登录
        if request.method == 'GET':
            goodsid = request.GET.get('goodsid')
            num = request.GET.get('num')

            # 判断商品是否已经加入用户购物车中
            # 1.存在，num增加
            # 2.不存在，添加购物车

            carts = Cart.objects.filter(user_id=userid, goods_id=goodsid)
            if carts.exists():
                # 用户存在，增加数量
                cart = carts.first()
                cart.num += int(num)
                cart.save()
            else:
                # 用户不存在，cart中新增用户购物车
                cart = Cart()
                cart.user_id = userid
                cart.goods_id = goodsid
                cart.num = int(num)
                cart.save()
        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 购物车中数据操作
# 数量+
def cart_num_add(request):
    data = {
        'status': 1,
        'msg': 'ok', }

    # 判断是否登录
    userid = request.session.get('userid')

    if not userid:
        # 未登录
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        # 登录成功
        if request.method == "GET":

            cartid = request.GET.get('cartid')

            # 数量+
            carts = Cart.objects.filter(id=cartid)

            if carts.exists():
                cart = carts.first()
                cart.num += 1
                cart.save()

                #
                data['num'] = cart.num

            else:
                data['status'] = -1
                data['msg'] = '购物车中没有该商品'

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误'
    return JsonResponse(data)


# 数量-
def cart_num_reduce(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid')

    if not userid:

        data = {
            'status': 0,
            'msg': '未登录'
        }
    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')

            # 数量
            carts = Cart.objects.filter(id=cartid)
            if carts.exists():
                cart = carts.first()
                if cart.num > 1:
                    cart.num -= 1
                cart.save()

                data['num'] = cart.num
            else:
                data['status'] = -1
                data['msg'] = '该商品不存在'
        else:
            data['status'] = -2
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 删除商品按钮
def cart_num_del(request):
    data = {
        'status': 1,
        'msg': '删除成功'
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')
            Cart.objects.filter(id=cartid).delete()

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 取消勾选/勾选
def cart_select(request):
    data = {
        'status': 1,
        'msg': 'ok', }

    # 判断是否登录
    userid = request.session.get('userid')

    if not userid:
        # 未登录
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        # 登录成功
        if request.method == "POST":

            cartid = request.POST.get('cartid')
            carts = Cart.objects.filter(id=cartid)

            if carts.exists():
                cart = carts.first()
                cart.is_select = not cart.is_select
                cart.save()
                data['select'] = cart.is_select
            else:
                data['status'] = -1
                data['msg'] = '购物车中不存在该商品'

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误'
    return JsonResponse(data)


# 全选/取消全选
def cart_allselect(request):
    data = {
        'status': 1,
        'msg': 'ok-取消全选', }

    # 判断是否登录
    userid = request.session.get('userid')

    if not userid:
        # 未登录
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        # 登录成功
        if request.method == "POST":
            action = request.POST.get('action')
            # print(action)
            # print(type(action)) <class 'str'>
            # print(action)
            # action = (action)
            # print(action)
            # print(type(action))

            # 取消全选
            if action == 'true':
                Cart.objects.filter(user_id=userid).update(is_select=False)
            # 全选
            else:
                Cart.objects.filter(user_id=userid, is_select=False).update(is_select=True)
                data['status'] = -1
                data['msg'] = 'ok-全选'

            #判断全选按钮✔是否存在
            """carts = Cart.objects.filter(user_id = userid)
            print(carts)
            for cart in carts:
                if not cart.is_select:
                    data = {'status':-4,'msg':'不打勾'}
                else:
                    data={'status':-5,'msg':'打勾'} """

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误'
    return JsonResponse(data)


# ******************************购物车功能***********************************


# 订单
def order(request, oid):
    order = Order.objects.get(id=oid)
    return render(request, 'order/order.html',{'order':order})


# 添加订单
def order_add(request):
    data = {
        'status': 1,
        'msg': 'ok'
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'POST':
            # 给订单表添加一条数据
            # 给订单添加多个商品
            order = Order()
            order.order_id = my_md5(str(uuid.uuid4()))  # 订单编号,在后端生成,随机且唯一
            order.user_id = userid
            order.save()

            # 将当前用户购物车中选中的商品添加到订单商品表
            carts = Cart.objects.filter(user_id=userid, is_select=True)

            if carts.exists():

                total = 0  # 订单总价
                for cart in carts:
                    order_goods = orderGoods()
                    order_goods.goods_id = cart.goods_id
                    order_goods.num = cart.num
                    order_goods.order_id = order.id
                    order_goods.price = cart.goods.price
                    order_goods.save()

                    total += order_goods.price * order_goods.num

                    # 订单总价
                    order.order_price = total
                    order.save()
            else:
                data['status'] = -2
                data['msg'] = 'cart中没有选中商品'


            #生成的订单成功后删除购物车
            carts.delete()

            # 将订单id返回
            data['orderid'] = order.id

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'
    return JsonResponse(data)


#修改订单状态
def order_change_status(request):
    data = {
        'status': 1,
        'msg': 'ok'
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'POST':
            orderid = request.POST.get('orderid')
            status = request.POST.get('status')
            print(status,userid)
            Order.objects.filter(id = orderid).update(order_status = status)


        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'
    return JsonResponse(data)


#待付款订单
def order_unpay(request):
    #是否登录
    userid = request.session.get('userid')
    if not userid:
        return redirect(reverse('axf:login'))

    # 获取所有未付款订单
    orders = Order.objects.filter(order_status=0,user_id = userid)
    return render(request,'order/order_unpay.html',{'orders':orders})


#待收货
def order_unreceive(request):
    #是否登录
    userid = request.session.get('userid')
    if not userid:
        return redirect(reverse('axf:login'))

    # 获取所有付款订单
    orders = Order.objects.filter(order_status=1,user_id = userid)
    return render(request,'order/order_unreceive.html',{'orders':orders})

