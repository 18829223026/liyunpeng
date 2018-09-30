from django.db import models

class Luntan1(models.Model):
    type_name = models.CharField(max_length=255, blank=True, null=True)
    clinck = models.CharField(max_length=255, blank=True, null=True)
    huifu = models.CharField(max_length=255, blank=True, null=True)
    anthor = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'luntan1'


class Rshouche1(models.Model):
    car_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    lucheng = models.CharField(max_length=255, blank=True, null=True)
    where_field = models.CharField(db_column='where_', max_length=255, blank=True, null=True)  # Field renamed because it ended with '_'.
    guige = models.CharField(max_length=255, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)
    url_field = models.CharField(db_column='url_', max_length=255, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'rshouche1'
