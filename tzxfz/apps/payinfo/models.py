from django.db import models
from shortuuidfield import ShortUUIDField

class Payinfo(models.Model):
    price = models.FloatField()
    path = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=100)

# def get_user():
#     from apps.xfzauth.models import User
#     return User.objects.first()

class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey('Payinfo',on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    # DO_NOTHING：在django中，不会做任何的处理。完全看数据库的关系
    buyer = models.ForeignKey("xfzauth.User",on_delete=models.DO_NOTHING)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1：代表的是支付宝。2：代表的是微信
    istype = models.SmallIntegerField(default=0)
    # 1：代表的是未支付。2：代表的是支付完成
    status = models.SmallIntegerField(default=1)