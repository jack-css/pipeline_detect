# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.http import JsonResponse
import base64  # for base64 encoding
import django_excel as excel
import os
import urllib
from polls import models
# def index(request):
#     return render(request, 'first.html')


def first_page(request):
    username = request.COOKIES.get('username')
    print('use',username)
    template = loader.get_template("polls/first.html")
    context = {
        "latest_question_list": '/static/img/deal_end.png'
    }
    return HttpResponse(template.render(context, request))
#
# def login(request):
#     template = loader.get_template("polls/login.html")
#     # detect_depair.from_path_main()
#     context = {
#         "latest_question_list": 1,
#     }
#     # models.User.objects.create(user_id = 1,account=123456,password='sx123456',name='特t')
#         # car_num='陕E-BV886', park_name='中医院', jinru_Date='2022-02-05',
#         #                        chuqu_Date='2022-02-06', time='1')
#     return HttpResponse(template.render(context, request))


def digital_map(request):
    template = loader.get_template("polls/digital_map.html")
    # detect_depair.from_path_main()
    context = {
        "latest_question_list": 1,
    }
    return HttpResponse(template.render(context, request))


def upload_data(request):
    template = loader.get_template("polls/upload_data.html")
    context = {
        "latest_question_list": 1,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def download_excel(request):
    import time
    temp_time = time.localtime()
    file_path = os.path.join('static/', 'my_data.xlsx')
    # print(temp_time.tm_min, temp_time.tm_sec, temp_time.tm_sec * 25)
    name = '检测'.encode('utf-8')
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = f'attachment; filename={name}{str(temp_time.tm_min) + str(temp_time.tm_sec) + str(temp_time.tm_sec * 25)}.xlsx'
        return response


def login(request):
    error_msg = []
    userid, username, password = [], [], []
    if request.POST:
        userid = request.POST['userid']
        username = request.POST['username']
        password = request.POST['password']
        print(userid, username, password)
    # users = models.User.objects.all()
    else:
        return render(request, 'polls/login.html')
    # 根据ID获取博客
    try:
        # 登录
        blog = models.User.objects.filter(account=userid)
        if blog:
            try:
                ret = models.User.objects.filter(account=userid, password=password)
                if ret:
                    request.set_cookie('username', 'johnDoe', max_age=24 * 60 * 60)
                    # return render(request, 'polls/first.html')
                    return first_page(request)
                else:
                    # 登录失败
                    error_msg = '用户名或密码错误，请重新输入！'
                    print('密码错误')
                return render(request, 'polls/login.html', {'error_msg': error_msg})
            except models.User.DoesNotExist:
                return render(request, 'polls/login.html', {'error_msg': error_msg})
        else:
            print('注册成功')
            models.User.objects.create(account=userid, password=password, name=username)
            return render(request, 'polls/login.html')
    finally:
        return render(request, 'polls/login.html', {'error_msg': error_msg})





