from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from board.models import Post
from rental.models import *


@csrf_exempt
def mypage_user(request):
    authuser = request.session.get('authUser')
    user = User.objects.get(member_id=authuser['member_id'])
    if request.method == "POST":
        user.overdue = 0
        user.save()
        return render(request, 'mypage/mypage_user.html', {'user':user})
    return render(request, 'mypage/mypage_user.html', {'user':user})


def mypage_useredit(request):
    authuser = request.session.get('authUser')
    user = User.objects.get(member_id=authuser['member_id'])
    response_data = {}
    if request.method == "POST":
        edit_id = request.POST.get('edit_id', None)
        edit_phone = request.POST.get('edit_phone', None)
        response_data['user'] = user
        if not edit_id:
            response_data['error'] = "아이디를 입력하시오."
        elif not edit_phone:
            response_data['error'] = "전화번호를 입력하시오."
        else:
            if User.objects.filter(phone=edit_phone).exclude(member_id=user.member_id):
                response_data['error'] = "이미 존재하는 전화번호입니다."
            if User.objects.filter(member_id=edit_id).exclude(phone=user.phone):
                response_data['error'] = "이미 존재하는 아이디입니다."
            else:
                user.phone = edit_phone
                user.member_id = edit_id

                if request.POST.get('another_address') :
                    user.address = request.POST.get('another_address')
                    user.address += " " + request.POST.get('another_address_detail')

                user.save()
                results = User.objects.filter(member_id=edit_id).filter(phone=edit_phone)
                authUser = results[0]
                request.session['authUser'] = model_to_dict(authUser)
                return render(request, 'mypage/mypage_user.html', {'user':user})
            return render(request, 'mypage/mypage_useredit.html', response_data)
    return render(request, 'mypage/mypage_useredit.html', {'user':user})


def mypage_game(request):
    authuser = request.session.get('authUser')
    user = User.objects.get(member_id=authuser['member_id'])
    user_grental = GameRental.objects.filter(member_id=user).order_by('-game_rental_id')
    user_greserve = GameReserve.objects.filter(member_id=user).order_by('-game_reserve_id')
    return render(request, 'mypage/mypage_game.html', {'user_grental': user_grental, 'user_greserve': user_greserve})


def mypage_device(request):
    authuser = request.session.get('authUser')
    user = User.objects.get(member_id=authuser['member_id'])
    user_drental = DeviceRental.objects.filter(member_id=user).order_by('-device_rental_id')
    user_dreserve = DeviceReserve.objects.filter(member_id=user).order_by('-device_reserve_id')

    return render(request, 'mypage/mypage_device.html', {'user_drental': user_drental, 'user_dreserve': user_dreserve,})


def mypage_like(request):
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    like_devices = RentalDevice.objects.filter(device_like=i)
    like_games = RentalGame.objects.filter(game_like=i)
    return render(request, 'mypage/mypage_like.html', {'like_devices': like_devices, 'like_games': like_games, 'i': i})


def mypage_Gdislike(request, g_id):
    g = RentalGame.objects.get(game_id=g_id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    g.game_like.remove(i)
    return redirect('mypage:mypage_like')


def mypage_Ddislike(request, d_id):
    d = RentalDevice.objects.get(device_id= d_id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    d.device_like.remove(i)
    return redirect('mypage:mypage_like')


def dreserve_delete(request, drs_id):
    drs = DeviceReserve.objects.get(device_reserve_id=drs_id)
    if DeviceReserve.objects.filter(device_id=drs.device_id).count() == 1:
            if DeviceRental.objects.filter(device_id=drs.device_id, overdue=None).count() == 0:
                rd = RentalDevice.objects.get(device_name=drs.device_id)
                rd.device_check = 0
                rd.save()
    else:
        drss = DeviceReserve.objects.filter(device_reserve_id__gt=drs_id, device_id=drs.device_id)
        for i in drss:
            i.device_due_date = i.device_due_date - timedelta(days=15)
            i.save()
    drs.delete()
    return redirect('mypage:mypage_device')


def device_return(request, dr_id):
    dr = DeviceRental.objects.get(device_rental_id=dr_id)
    drs = DeviceReserve.objects.filter(device_id=dr.device_id)
    if datetime.now().date() < dr.dreturn_date:
        dr.overdue = 0
        date = dr.dreturn_date - datetime.now().date()
    else:
        date = datetime.now().date() - dr.dreturn_date
        dr.overdue = date.days + 1
        authuser = request.session.get('authUser')
        user = User.objects.get(member_id=authuser['member_id'])
        user.overdue = user.overdue + dr.overdue
        user.save()

    if drs.count() == 0:
        rd = RentalDevice.objects.get(device_name=dr.device_id)
        rd.device_check = 0
        rd.save()

    dr.dreturn_date = datetime.now().date() + timedelta(days=1)
    dr.save()

    for i in drs:
        i.device_due_date = i.device_due_date - timedelta(days=date.days-1)
        i.save()

    return redirect('mypage:mypage_device')


def greserve_delete(request, grs_id):
    grs = GameReserve.objects.get(game_reserve_id=grs_id)

    if GameReserve.objects.filter(game_id=grs.game_id).count() == 1:
        if GameRental.objects.filter(game_id=grs.game_id, overdue=None).count() == 0:
            rg = RentalGame.objects.get(game_name=grs.game_id)
            rg.game_stock = rg.game_stock + 1
            rg.save()
    else:
        grss = GameReserve.objects.filter(game_reserve_id__gt=grs_id, game_id=grs.game_id)
        for i in grss:
            i.game_due_date = GameReserve.objects.get(game_reserve_id=i.game_reserve_id-1).game_due_date
            i.save()

    grs.delete()
    return redirect('mypage:mypage_game')


def game_return(request, gr_id):
    gr = GameRental.objects.get(game_rental_id=gr_id)

    grs = GameReserve.objects.filter(game_id=gr.game_id)

    gr.greturn_date = datetime.now().date() + timedelta(days=1)
    if datetime.now().date() < gr.greturn_date:
        gr.overdue = 0

        if grs.count() == 0:
            rg = RentalGame.objects.get(game_name=gr.game_id)
            rg.game_stock = rg.game_stock + 1
            rg.save()
        else:
            grs_f = grs.first()
            grs_f.game_due_date = gr.greturn_date + timedelta(days=2)
            grs_f.save()
    else:
        date = datetime.now().date() - gr.greturn_date
        gr.overdue = date.days
    gr.save()

    return redirect('mypage:mypage_game')


def mypage_board(request):
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    b = Post.objects.filter(member_id=i)
    page = request.GET.get('page', '1')
    paginator = Paginator(b, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return render(request, 'mypage/mypage_board.html', {'b': page_obj,})