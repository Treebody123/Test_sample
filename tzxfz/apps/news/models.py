from django.db import models

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


# aware time：清醒的时间（清醒的知道自己这个时间代表的是哪个时区的）
# navie time：幼稚的时间（不知道自己的时间代表的是哪个时区）

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey("NewsCategory",on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey("xfzauth.User",on_delete=models.SET_NULL,null=True)

    class Meta:
        #以后News.objects提取数据的时候，就会自动的按照列表中指定的字段排序
        # 如果不加负号，那么默认就是按照从小到大正序排序
        # 如果加上一个负号，就会按照从大到小倒序排序
        ordering = ['-pub_time']

class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey("News",on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']


class Banner(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField(default=0)
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']