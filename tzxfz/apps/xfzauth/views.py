#encoding: utf-8

from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from utils.captcha.hycaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from utils.aliyunsdk import aliyun
from .models import User
from utils import restful


class LoginView(View):
    def get(self,request):
        return render(request,'auth/login.html')

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone")
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request,username=telephone,password=password)
            if user:
                login(request,user)
                if remember:
                    # 如果设置过期时间为None，那么就会使用默认的过期时间
                    # 默认的过期时间是2个礼拜，也就是14天
                    request.session.set_expiry(None)
                else:
                    # 如果设置过期时间为0，那么浏览器关闭以后就会结束
                    request.session.set_expiry(0)
                # 如果登录成功，让他跳转到首页
                return redirect(reverse('news:index'))
            else:
                messages.info(request,'用户名或密码错误！')
                return redirect(reverse('xfzauth:login'))
        else:
            messages.info(request,'表单失败！')
            return redirect(reverse('xfzauth:login'))


# Form表单版本的注册代码
# class RegisterView(View):
#     def get(self,request):
#         return render(request,'auth/register.html')
#
#     def post(self,request):
#         form = RegisterForm(request.POST)
#         if form.is_valid() and form.validate_data(request):
#             telephone = form.cleaned_data.get('telephone')
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = User.objects.create_user(telephone=telephone,username=username,password=password)
#             login(request,user)
#             return redirect(reverse('news:index'))
#         else:
#             # print(type(form.errors))
#             # print(form.errors.get_json_data())
#             # {"telephone":[{"message":"手机号码个数必须为11位！"}]}
#             message = form.get_error()
#             messages.info(request,message)
#             return redirect(reverse('xfzauth:register'))

# ajax请求版本的注册代码
class RegisterView(View):
    def get(self,request):
        return render(request,'auth/register.html')

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.validate_data(request):
            # 先验证数据是否是合法的
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print("手机号码：%s"%telephone)
            user = User.objects.create_user(telephone=telephone,username=username,password=password)
            login(request,user)
            return restful.ok()
        else:
            message = form.get_error()
            return restful.params_error(message=message)

def logout_view(request):
    logout(request)
    return redirect('/')


def img_captcha(request):
    text,image = Captcha.gene_code()
    # image不是一个HttpResponse可以识别的对象
    # 因此先要将image变成一个数据流才能放到HttpResponse上
    # BytesIO：相当于一个管道，可以用来存储字节流的
    out = BytesIO()
    image.save(out,'png')
    # 将文件指针设置到0的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    request.session['img_captcha'] = text

    return response


def sms_captcha(request):
    code = Captcha.gene_text()
    # /accoutn/sms_captcha/?telephone=12345678900
    telephone = request.GET.get('telephone')
    request.session['sms_captcha'] = code
    # result = aliyun.send_sms(telephone,code=code)
    print('短信验证码：%s'%code)
    return HttpResponse('success')

