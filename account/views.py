from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

from account.models import User


def login(request):
    response_data = {}
    if request.method == "POST":
        member_id = request.POST.get('member_id', None)
        password = request.POST.get('password', None)

        if not (member_id and password):
            response_data['error'] = "아이디와 비밀번호를 모두 입력하시오."
        else:
            results = User.objects.filter(member_id=request.POST['member_id']).filter(password=request.POST['password'])

            # 로그인 실패
            if len(results) == 0:
                response_data['error'] = "로그인이 실패 했습니다."
            else:
                # 로그인 처리
                authUser = results[0]
                request.session['authUser'] = model_to_dict(authUser)

                return HttpResponseRedirect('/')
        return render(request, 'account/log_in.html', response_data)
    else:
        return render(request, 'account/log_in.html')


def logout(request):
    auth.logout(request)
    return redirect('home:home')


def register_done(request):
    return render(request, 'account/register_done.html')


def register(request):
    if request.method == 'POST':
        if request.POST['1st_password'] == request.POST['2st_password']:
            user = User()
            if not request.POST['member_name']:
                return HttpResponseRedirect('/account/register?result=namefail')
            elif not request.POST['member_id']:
                return HttpResponseRedirect('/account/register?result=idfail')
            elif not request.POST['phone']:
                return HttpResponseRedirect('/account/register?result=phonefail')
            else:
                if User.objects.filter(member_id=request.POST['member_id']):
                    return HttpResponseRedirect('/account/register?result=id_repeat')
                else:
                    user.member_id = request.POST['member_id']

                if User.objects.filter(phone=request.POST['phone']):
                    return HttpResponseRedirect('/account/register?result=phone_repeat')
                else:
                    user.phone = request.POST['phone']
                user.member_name = request.POST['member_name']
                user.password = request.POST['1st_password']
                user.address = request.POST['address']
                user.address += " " + request.POST['address_detail']
                user.overdue = 0
                user.save()
            return render(request, 'account/register_done.html')
        else:
            return HttpResponseRedirect('/account/register?result=passfail')
    else:
        return render(request, 'account/register.html')


@csrf_exempt
def find_id(request):
    response_data = {}
    if request.method == "POST":
        member_name = request.POST.get('member_name', None)
        phone = request.POST.get('phone', None)

        if not (member_name and phone):
            response_data['error'] = "이름과 전화번호를 모두 입력하시오."
        else:
            results = User.objects.filter(member_name=request.POST['member_name']).filter(phone=request.POST['phone'])

            if len(results) == 0:
                response_data['error'] = "이름 혹은 전화번호가 등록되어 있지 않습니다."
            else:
                user = results.first()
                response_data['success'] = user.member_id
            return render(request, 'account/find_id.html', response_data)
    return render(request, 'account/find_id.html')


@csrf_exempt
def find_pw(request):
    response_data = {}
    if request.method == "POST":
        member_id = request.POST.get('member_id', None)

        if not member_id:
            response_data['error'] = "아이디를 입력하시오."
        else:
            results = User.objects.filter(member_id=request.POST['member_id'])

            if len(results) == 0:
                return HttpResponseRedirect('/account/find_pw?result=fail')
            else:
                user = results.first()
                response_data['success'] = user.password
            return render(request, 'account/find_pw.html', response_data)
    return render(request, 'account/find_pw.html')