from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
import re
from apps.user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
class RegisterView(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        # 获取输入的内容
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 判断是否输入正确

        # all 函数 如果里面的可迭代的 有为空的 返回False
        # 判断是否输入完整
        if not all([username,password,email]):
            return render(request, 'register.html', {'error': '请输入完整'})

        # 判断邮箱格式
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request, 'register.html', {'error': '邮箱格式不正确'})

        # 判断是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'error': '请同意协议'})
        # 判断是否用户名重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request,'register.html',{'error':'该用户名以注册'})

        # 把数据提交到数据库
        user = User.objects.create_user(username,password,email)
        user.is_active = 0
        user.save()
        # return redirect(reverse('goods:index'))
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confit':user.id}
        token = serializer.dumps(info)
        token = token.decode()
        # send_mail(邮件标题, 邮件文本, 发件人, 收件人列表, html_message=html邮件内容)
        subject = '天天卖菜'
        message = '123'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject,message,from_email,recipient_list)
        return redirect(reverse('goods:index'))



class ActiveView(View):
        # 激活
    def get(self,request,token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confit']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('login.html')) #跳到登陆页面
        except SignatureExpired as e:
            return HttpResponse('激活链接过期')

