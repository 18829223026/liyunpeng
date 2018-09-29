from django.db import models


class User(models.Model):
    """用户个人信息"""
    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name
        ordering = ['-last_login']

    email = models.EmailField('邮箱', max_length=100)
    username = models.CharField('用户名', max_length=60)
    password = models.CharField('密码', max_length=32)
    sex = models.SmallIntegerField(choices=[(0, '女'), (1, '男')], verbose_name='性别')
    birthday = models.DateField(verbose_name='生日')
    date_created = models.DateTimeField(verbose_name='注册日期', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='最后登录', null=True)
    last_updated = models.DateTimeField(verbose_name='最后更新', auto_now=True)

    def __str__(self):
        return self.username



class Category(models.Model):
    """商品分类"""
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='父分类', null=True, blank=True)
    name = models.CharField('名称', max_length=30)
    keywords = models.CharField('关键字', max_length=200)
    description = models.CharField('描述', max_length=100)
    sort_order = models.IntegerField('排序')
    is_show = models.BooleanField('是否展示')

    def __str__(self):
        return self.name


class Goods(models.Model):
    """商品信息"""
    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    name = models.CharField('名称', max_length=30)
    stock = models.IntegerField('库存')
    market_price = models.DecimalField('市场价', max_digits=10, decimal_places=2)
    sell_price = models.DecimalField('售价', max_digits=10, decimal_places=2)
    keywords = models.CharField('关键字', max_length=200)
    brief = models.CharField('简介', max_length=200)
    description = models.TextField('详情')
    is_sale = models.BooleanField('是否售卖', default=True)
    is_best = models.BooleanField('是否精品', default=True)
    is_new = models.BooleanField('是否新品', default=True)
    is_hot = models.BooleanField('是否热卖', default=True)
    last_update = models.DateTimeField('最后更新', auto_now=True)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    def __str__(self):
        return self.name


class OrderInfo(models.Model):
    """订单信息"""
    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ManyToManyField(Goods, through='OrderGoods', through_fields=('order_info', 'goods'), verbose_name='商品')
    status = models.SmallIntegerField('订单状态', choices=[(0, '未确认'), (1, '确认'), (2, '已取消'), (3, '无效'), (4, '退货')])
    pay_status = models.SmallIntegerField('支付状态', choices=[(0, '未付款'), (1, '付款中'), (2, '已付款')])
    shipping_status = models.SmallIntegerField('配送状态', choices=[(0, '未发货'), (1, '已发货'), (2, '已收货'), (3, '退货 ')])
    date_created = models.DateTimeField(auto_now=True,verbose_name='下单日期')

class OrderGoods(models.Model):
    """订单商品（订单和商品是多对多关系，该表是中间表）"""
    order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单ID')
    goods = models.ForeignKey(Goods, '商品ID')
    number = models.SmallIntegerField('数量')
    market_price = models.DecimalField('市场价', max_digits=10, decimal_places=2)
    sell_price = models.DecimalField('售价', max_digits=10, decimal_places=2)
    add_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_update = models.DateTimeField('最后更新', auto_now=True)




