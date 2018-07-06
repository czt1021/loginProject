import hashlib
import uuid

import os

from django.core.paginator import Paginator
from django.http import request, JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from loginProject import settings
from mainapp.models import User


def home(req):
    return render(req, "home.html")

def newFileName(contentType):
    fileName = crypt(str(uuid.uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName  = '.png'
    return fileName + extName

def newToken(username):
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4()) + username).encode())
    return md5.hexdigest()


def crypt(pwd, cryName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()


def home_logined(req):
    token = req.COOKIES.get('token')
    if not token:
        return redirect('/main/login')
        # 从session中读取登录用户信息

    return render(req, 'home_logined.html',
                  {'user': User.objects.filter(token=token).last()})
    # return render(req,'home_logined.html')


def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')

    username = req.POST.get('username')
    passwd = req.POST.get('passwd')

    qs = User.objects.filter(username=username,
                             passwd=crypt(passwd))

    if qs.exists():
        req.session['qs'] = qs.last().toDict()
        user = qs.first()
        user.token = newToken(user.username)
        user.save()
        resp = redirect('/main/home_logined')
        resp.set_cookie('token', user.token)
        return resp
    else:
        return render(req, 'login.html',
                      {'error_msg': '用户名或口令错误!'})


def regist(req):
    if req.method == 'GET':
        return render(req, 'register.html')

    user = User()
    user.username = req.POST.get('username')
    user.passwd = crypt(req.POST.get('passwd'))

    user.token = newToken(user.username)
    user.photo = req.FILES['photo']

    uploadFile = req.FILES.get('photo')
    saveFileName = newFileName(uploadFile.content_type)
    saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)

    with open(saveFilePath, 'wb') as f:
        for part in uploadFile.chunks():
            f.write(part)
            f.flush()
    user.img = saveFilePath
    user.token = newToken(user.username)

    user.save()

    resp = redirect('/main/login')
    resp.set_cookie('token', user.token)

    return resp


def userinfo_mod(req):
    if req.method == 'GET':
        return render(req, 'userinfo_mod.html')


    username = req.POST.get('username')
    # photo = req.FILES['photo']
    photo = req.FILES.get('photo')
    print('1111')

    if username:
        print('222')
        print(username)
        User.objects.filter(username=username).update(username=username,photo=photo)
    else:
        print('3333')
        loginUser = User.objects.filter(token=req.COOKIES.get('token')).last()
        User.objects.create(username=username,photo=photo)
    print('5555')
    resp = redirect('/main/home_logined')
    return resp



# def userinfo_mod(req):
#     if req.method == 'GET':
#         return render(req,'home_logined.html')
#
#     user = User()
#     user.username = req.POST.get('username')
#     user.token = newToken(user.username)
#     user.photo = req.FILES['photo']
#
#     token = req.COOKIES.get('token')
#
#     loginUserDict = req.session.get('qs')
#     print(loginUserDict)
#     data = {}
#     if loginUserDict:
#         data['login_username'] = loginUserDict['username']
#         data['login_photo'] = loginUserDict['photo']
#         data['login_id'] = loginUserDict['id']
#         print(data.get('login_username'))
#     # return render(req, 'users/home.html',
#     #               {'data': data})
#
#     # resp = redirect('/main/home_logined')
#     username = req.POST.get('username')
#     # passwd = req.POST.get('passwd')
#     photo = req.POST.get('photo')
#     qs = User.objects.filter(username=username,
#
#                              photo=photo)
#     if qs.exists():
#         user = qs.first()
#         User.objects.filter(id=1).update(phone=data['login_photo'])
#         resp = redirect('/main/login')
#         resp.set_cookie('token', user.token)
#     return render(req, 'userinfo_mod.html',
#                   {'user': User.objects.filter(token=token).last(),
#                    'data': data})

def upload(req):
    # 上传文件
    uploadFile = req.FILES.get('photo')
    print(uploadFile.__dict__)  # content_type
    user = User()
    saveFileName = str(uuid.uuid4()) + ".jpg"
    saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)

    with open(saveFilePath, 'wb') as f:
        for part in uploadFile.chunks():
            f.write(part)
            f.flush()
    user.img = saveFilePath
    # user.token = newToken(user.userName)
    user.save()
    # resp = HttpResponseRedirect('/app/home')
    # resp.set_cookie('token', user.token)
    # return resp
    return JsonResponse({"path": saveFileName})


def logout(req):
    req.session.clear()
    return redirect('/main')


def list(req, page_num=1):
    users = User.objects.all()
    paginator = Paginator(users, 5)  # 创建分页器
    page = paginator.page(page_num)  # 获取第一页

    return render(req, "home_logined_collected.html", {
        "users": page.object_list,  # 本页数据
        "current_page": page_num,  # 分页的页面
        "page_range": paginator.page_range  # 分页的范围
    })


def add(req):
    return render(req, "userinfo_mod.html")
