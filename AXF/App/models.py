from django.db import models


# 父类
class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=30)
    trackid = models.CharField(max_length=20)

    class Meta:
        abstract = True  # 设置为抽象类,不会生成表


# 首页轮播数据
class HomeWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


# 首页-导航
class HomeNav(Main):
    class Meta:
        db_table = 'axf_nav'


# 首页-必购
class HomeMustBuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'


# 首页-商品
class HomeShop(Main):
    class Meta:
        db_table = 'axf_shop'

#商品详情
class HomeShow(Main):
    categoryid = models.CharField(max_length=20)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=20)
    productid1 = models.CharField(max_length=20)
    longname1 = models.CharField(max_length=40)
    price1 = models.FloatField(max_length=20)
    marketprice1 = models.CharField(max_length=20)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=20)
    productid2 = models.CharField(max_length=20)
    longname2 = models.CharField(max_length=40)
    price2 = models.FloatField(max_length=20)
    marketprice2 = models.CharField(max_length=20)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=20)
    productid3 = models.CharField(max_length=20)
    longname3 = models.CharField(max_length=40)
    price3 = models.FloatField(max_length=20)
    marketprice3 = models.CharField(max_length=20)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购-商品分类
class FoodType(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'

#商品信息
class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=50)
    productlongname = models.CharField(max_length=200)

    isxf = models.BooleanField(default=False)
    pmdesc = models.IntegerField()
    specifics = models.CharField(max_length=20)
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.CharField(max_length=20)
    childcid = models.CharField(max_length=40)
    childcidname = models.CharField(max_length=40)
    dealerid = models.CharField(max_length=40)
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'


#用户表
class User(models.Model):
    name = models.CharField(max_length=20,unique=True)
    passwd = models.CharField(max_length=40)
    email = models.EmailField()
    icon = models.CharField(max_length=200,default='')
    gender = models.BooleanField(default=True)
    is_delete =models.BooleanField(default=False)



#购物车
class Cart(models.Model):
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)



#订单
class Order(models.Model):

    order_id = models.CharField(max_length=32,unique=True)
    order_create = models.DateTimeField(auto_now_add=True)
    order_price = models.FloatField(default=0)
    user = models.ForeignKey(User)

    #订单状态:0表示未支付，1表示待收货，2表示待评价，3表示订单完成
    order_status = models.CharField(max_length=10,default=0)

#订单商品表
class orderGoods(models.Model):
    goods = models.ForeignKey(Goods)
    num = models.PositiveIntegerField(default=1)
    price =models.FloatField(default=0)
    order = models.ForeignKey(Order)

