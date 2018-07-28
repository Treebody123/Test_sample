from django.shortcuts import render
from .models import News,NewsCategory,Banner
from django.views.decorators.http import require_GET,require_POST
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer,CommentSerizlizer
from django.http import Http404
from .forms import AddCommentForm
from .models import Comment
# login_required：只能针对传统的页面跳转（如果没有登录，就跳转到login_url指定的页面）
# 但是他不能处理这种ajax请求。就是说如果通过ajax请求去访问一个需要授权的页面
# 那么这个装饰器的页面跳转功能就不行了
from django.contrib.auth.decorators import login_required
from apps.xfzauth.decorators import xfz_login_required
from django.core.paginator import Paginator
from django.db.models import Q


# 通过视图函数找其对应的url，那么这种就叫做url反转
# 通过url来找到视图函数

def index(request):
    newses = News.objects.select_related('category','author')[0:settings.ONE_PAGE_NEWS_COUNT]
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': banners
    }
    return render(request,'news/index.html',context=context)

@require_GET
def news_list(request):
    # /news/list/?p=3
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))
    # offer,limit 0+10=10,10+10=20
    start = settings.ONE_PAGE_NEWS_COUNT*(page-1)
    end = start + settings.ONE_PAGE_NEWS_COUNT
    # newses：QuerySet -> [News(),News()]
    # [{"title":"","content":''},{"title":"","content":''}]
    # newses = list(News.objects.all()[start:end].values())
    # print(type(newses))
    # for news in newses:
    #     print(type(news))
    #     break
    # values：
    # 将QuerySet中的模型对象（比如News()对象）转换为字典
    # 0,10:0,1,2,3,4,5,6,
    if category_id == 0:
        # 如果category_id=0，说明没有传cateogry_id过来
        newses = News.objects.all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start:end]
    serizlizer = NewsSerializer(newses,many=True)
    return restful.result(data=serizlizer.data)


# 如果在url中定义了参数
# 那么在视图函数中也要定义相应的参数
def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category', 'author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404

@require_POST
@xfz_login_required
def add_comment(request):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_error())



def search(request):
    q = request.GET.get('q')
    if q:
        # title或者content中包含了搜索的关键字，那么就返回
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context = {
            'newses': newses
        }
    else:
        context = {}
    return render(request,'news/search.html',context=context)
