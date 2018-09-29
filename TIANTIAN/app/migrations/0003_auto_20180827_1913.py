# Generated by Django 2.1 on 2018-08-27 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(verbose_name='数量')),
                ('goods', models.ForeignKey(on_delete='商品ID', to='app.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_status', models.SmallIntegerField(choices=[(0, '未付款'), (1, '已付款')], verbose_name='支付状态')),
                ('shipping_status', models.SmallIntegerField(choices=[(0, '未发货'), (1, '已发货'), (2, '已收货'), (3, '退货 ')], verbose_name='配送状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('goods', models.ManyToManyField(through='app.OrderGoods', to='app.Goods', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User', verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '订单信息',
                'verbose_name': '订单信息',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrderInfo', verbose_name='订单ID'),
        ),
    ]