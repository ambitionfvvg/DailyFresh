# encoding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from .models import  *
from django.http import HttpResponseRedirect

# Create your views here.

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):

    # 获取属性的值
    name = request.POST['user_name']
    pwd1 = request.POST['pwd']
    pwd2 = request.POST['cpwd']
    email = request.POST['email']

    # 判断输入是否为空
    if (len(name)==0 & len(pwd1)==0 or len(email)==0):
        context = {'error': '有参数为空，请检查', }
        return render(request, 'df_user/register.html', context)

    # 查看用户名是否已被使用
    count = UserInfo.objects.filter(uname=name).count()

    if count !=0:
        context = {'error':'用户名已被使用,请修改',}
        return render(request, 'df_user/register.html',context)

    # 比较两次的密码是否一样
    if pwd1 !=pwd2:
        return redirect('/user/register')

    # 对密码进行加密处理
    s1 = sha1()
    s1.update(pwd1)
    pwd = s1.hexdigest()

    # 创建对象并给属性赋值
    user = UserInfo()
    user.uname = name
    user.upwd = pwd
    user.uemail = email

    user.save()

    return render(request,'df_user/login.html')


def login(request):

    # 从cookies 中获取用户名
    uname = request.COOKIES.get('uname','')

    context = {'title':'用户登录',
               'error_name':0,
               'error_pwd': 0,
               'uname': uname,}

    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 获取用户名和密码
    name = request.POST['username']
    pwd = request.POST['pwd']
    jizhu = request.POST.get('jizhu',0)

    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=name)

    # 检查用户名是否存在
    if len(users)==1:
        s1 = sha1()
        s1.update(pwd)
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            #记住用户名
            if jizhu != 0:
                red.set_cookie('uname',name)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = name
            return red
        else:
            context = {'title':'用户登录',
                       'error_name':0,
                       'error_pwd':1,
                       'uname':name,
                       'upwd':pwd}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title': '用户登录',
                   'error_name': 1,
                   'error_pwd': 0,
                   'uname': name,
                   'upwd': pwd}
        return render(request, 'df_user/login.html', context)


def info(request):

    user = UserInfo.objects.filter(id=request.session['user_id'])
    uname = request.session['user_name']
    uphone = user[0].uphone
    uemail = user[0].uemail

    context = {'uname':uname,
               'uemail':uemail,

    }

    return render(request,'df_user/user_center_info.html',context)

def orders(request):

    return render(request,'df_user/user_center_order.html')


def site(request):
    # user = UserInfo.objects.filter(id=request.session['user_id'])
    user = UserInfo.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        user.ushou = request.POST['ushou']
        user.uaddress = request.POST['uaddress']
        user.uyoubian = request.POST['uyoubian']
        user.uphone = request.POST['uphone']
        user.save()

    context = {'title':'用户中心','user':user}

    return render(request,'df_user/user_center_site.html',context)



