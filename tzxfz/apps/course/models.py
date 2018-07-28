from django.db import models

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)

class Teacher(models.Model):
    username = models.CharField(max_length=100)
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()
    avatar = models.URLField()

class Course(models.Model):
    title = models.CharField(max_length=100)
    # 视频的链接
    video_url = models.URLField()
    # 封面图的链接
    cover_url = models.URLField()
    price = models.FloatField()
    # 这个持续时间代表的是秒
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey("Teacher",on_delete=models.DO_NOTHING,null=True)


class CourseOrder(models.Model):
    pub_time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    # 1：代表的是未支付。2：代表的是支付成功
    status = models.SmallIntegerField()
    course = models.ForeignKey("Course",on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("xfzauth.User",on_delete=models.DO_NOTHING)
    # 1：代表的是支付宝支付。2：代表的是微信支付。0：代表的是未知
    istype = models.SmallIntegerField(default=0)

