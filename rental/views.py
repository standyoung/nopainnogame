import random
from datetime import timedelta
import datetime

from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.dateparse import parse_date
from django.utils.datetime_safe import datetime
from django.core.paginator import Paginator

from .models import *
# Create your views here.


def device_list(request, d_values=None):
    current_value = None
    device_values = DeviceValues.objects.all()
    devices = RentalDevice.objects.all()
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])

    page = request.GET.get('page', '1')  # 페이지
    if d_values:
        current_value = get_object_or_404(DeviceValues, values=d_values)
        devices = devices.filter(device_value=current_value)

    device_sort = request.GET.get('device_sort')
    if device_sort == '01':
        devices = devices.annotate(d_likes=Count('device_like')).order_by('-d_likes')
    elif device_sort == '02':
        devices = devices.order_by('device_rfee')
    elif device_sort == '03':
        devices = devices.order_by('-device_rfee')
    elif device_sort == '04':
        devices = devices.order_by('-device_pub')

    device_check = request.GET.get('device_check')
    dc = None
    if device_check:
        devices = devices.filter(device_check=0)
        dc = 1
    else:
        dc = None

    paginator = Paginator(devices, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)

    return render(request, 'rental/device_list.html',
                  {'current_value': current_value, 'device_values': device_values, 'devices': page_obj, 'i': i, 'dc': dc})


def device_detail(request, d_id, d_name=None):
    device = get_object_or_404(RentalDevice, device_id=d_id, device_name=d_name)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])

    command_games = list(RentalGame.objects.filter(device_value=device.device_value))
    if len(command_games) < 5:
        command_games = random.sample(command_games, len(command_games))
    else:
        command_games = random.sample(command_games, 5)

    if DeviceRental.objects.filter(member_id=i, overdue=None).count() > 0:
        already = True
    else:
        already = False
    return render(request, 'rental/device_detail.html', {'device': device, 'authuser': authuser, 'already': already, 'command_games':command_games})


def device_like(request, d_id):
    d = get_object_or_404(RentalDevice, device_id=d_id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    if i in d.device_like.all():
        d.device_like.remove(i)
    else:
        d.device_like.add(i)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def device_rental(request, d_id):
    device = get_object_or_404(RentalDevice, device_id=d_id)
    authuser = request.session.get('authUser')
    tomorrow = get_drental_date().strftime('%Y.%m.%d')
    return_date = get_drental_date() + timedelta(days=15)
    return_date_p = return_date.strftime('%Y.%m.%d')
    if request.method == 'POST':
        d_rent = DeviceRental()
        d = RentalDevice.objects.get(device_id=d_id)
        d_rent.device_id = d
        l_check = DeviceRental.objects.last()
        if l_check == None:
            d_rent.device_rental_id = 1
        else:
            l = DeviceRental.objects.latest('device_rental_id')
            d_rent.device_rental_id = l.device_rental_id + 1
        if not request.POST['another_address']:
            d_rent.daddress = authuser['address']
        else:
            d_rent.daddress = request.POST['another_address']
            d_rent.daddress += " " + request.POST['another_address_detail']
        i = User.objects.get(member_id=authuser['member_id'])
        d_rent.member_id = i
        d_rent.dreturn_date = return_date
        d_rent.save()

        device.device_check = 1
        device.save()

        return redirect('/rental/rental_done')
    else:
        return render(request, 'rental/device_rental.html',
                      {'authuser': authuser, 'tomorrow': tomorrow, 'return_date': return_date_p, 'device': device,})


def device_reserve(request, d_id):
    device = get_object_or_404(RentalDevice, device_id=d_id)
    dr = DeviceRental.objects.filter(device_id=d_id)
    dr = dr.last()
    device_reserve_count = DeviceReserve.objects.filter(device_id=d_id).count()
    today = datetime.now().date()
    overdue = False
    if device_reserve_count == 0:
        if today > dr.dreturn_date:
            due_date = today + timedelta(days=4)
            overdue = True
        else:
            due_date = dr.dreturn_date + timedelta(days=2)
    else:
        drs = DeviceReserve.objects.filter(device_id=d_id)
        c = 1 + drs.count()*16
        due_date = dr.dreturn_date + timedelta(days=c)
    due_date_p = due_date.strftime('%Y.%m.%d')
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    command_games = list(RentalGame.objects.filter(device_value=device.device_value))
    if len(command_games) < 5:
        command_games = random.sample(command_games, len(command_games))
    else:
        command_games = random.sample(command_games, 5)
    if request.method == 'POST':
        d_reserve = DeviceReserve()
        dd = RentalDevice.objects.get(device_id=d_id)
        d_reserve.device_id = dd
        l_check = DeviceReserve.objects.last()
        if l_check == None:
            d_reserve.device_reserve_id = 1
        else:
            l = DeviceReserve.objects.latest('device_reserve_id')
            d_reserve.device_reserve_id = l.device_reserve_id + 1

        i = User.objects.get(member_id=authuser['member_id'])
        d_reserve.member_id = i

        d_reserve.device_due_date = due_date

        d_reserve.save()

        device.device_check = 1
        device.save()

        return redirect('/rental/reserve_done')
    else:
        u_already = DeviceReserve.objects.filter(member_id=i).count()
        due_start = due_date - timedelta(days=2)
        due_end = due_date - timedelta(days=1)
        return render(request, 'reserve/device_reserve.html',
                      {'device': device, 'due_start': due_start, 'due_end': due_end, 'due_date': due_date_p, 'authuser': authuser,
                       'u_already': u_already, 'device_reserve_count': device_reserve_count, 'overdue': overdue, 'command_games':command_games})


def game_list(request, g_device=None, g_genre=None):
    current_device = None
    game_devices = DeviceValues.objects.all()

    current_genre = None
    game_genres = Genre.objects.all()

    games = RentalGame.objects.all()
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    page = request.GET.get('page', '1')  # 페이지

    if g_device:
        current_device = get_object_or_404(DeviceValues, values=g_device)
        games = games.filter(device_value=current_device)

    if g_genre:
        current_genre = get_object_or_404(Genre, genre=g_genre)
        games = games.filter(genre=current_genre)

    game_sort = request.GET.get('game_sort')
    if game_sort == '01':
        games = games.annotate(g_likes=Count('game_like')).order_by('-g_likes')
    elif game_sort == '02':
        games = games.order_by('game_rfee')
    elif game_sort == '03':
        games = games.order_by('-game_rfee')

    game_check = request.GET.get('game_check')
    gc = None
    if game_check:
        games = games.exclude(game_stock=0)
        gc = 1

    paginator = Paginator(games, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)

    return render(request, 'rental/game_list.html',
                  {'current_device': current_device, 'game_devices': game_devices, 'games': page_obj, 'i': i, 'current_genre': current_genre, 'game_genres': game_genres, 'gc': gc})


def game_like(request, g_id):
    g = get_object_or_404(RentalGame, game_id=g_id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    if i in g.game_like.all():
        g.game_like.remove(i)
    else:
        g.game_like.add(i)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def game_detail(request, g_id):
    game = get_object_or_404(RentalGame, game_id=g_id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    command_games = list(RentalGame.objects.filter(genre=game.genre).exclude(game_id=g_id))
    if len(command_games) < 5:
        command_games = random.sample(command_games, len(command_games))
    else:
        command_games = random.sample(command_games, 5)
    if GameRental.objects.filter(game_id=g_id, member_id=i, overdue=None).count() > 0:
        already = True
    else:
        already = False
    return render(request, 'rental/game_detail.html', {'game': game, 'authuser': authuser, 'already': already, 'command_games': command_games},)


def game_rental(request, g_id):
    game = get_object_or_404(RentalGame, game_id=g_id)
    authuser = request.session.get('authUser')
    tomorrow = get_drental_date().strftime('%Y.%m.%d')
    return_date = get_drental_date() + timedelta(days=15)
    return_date_p = return_date.strftime('%Y.%m.%d')
    if request.method == 'POST':
        g_rent = GameRental()
        g = RentalGame.objects.get(game_id=g_id)
        g_rent.game_id = g
        l_check = GameRental.objects.last()
        if l_check is None:
            g_rent.game_rental_id = 1
        else:
            l = GameRental.objects.latest('game_rental_id')
            g_rent.game_rental_id = l.game_rental_id + 1
        if not request.POST['another_address']:
            g_rent.gaddress = authuser['address']
        else:
            g_rent.gaddress = request.POST['another_address']

        i = User.objects.get(member_id=authuser['member_id'])
        g_rent.member_id = i
        g_rent.greturn_date = return_date
        g_rent.save()

        game.game_stock = game.game_stock - 1
        game.save()

        return redirect('/rental/rental_done')
    else:
        return render(request, 'rental/game_rental.html',
                      {'authuser': authuser, 'tomorrow': tomorrow, 'return_date': return_date_p, 'game': game})


def game_reserve(request, g_id):
    game = get_object_or_404(RentalGame, game_id=g_id)
    gr = GameRental.objects.filter(game_id=g_id, overdue=None)
    game_reserve_count = GameReserve.objects.filter(game_id=g_id).count()
    today = datetime.now().date()
    overdue = False
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    command_games = list(RentalGame.objects.filter(genre=game.genre).exclude(game_id=g_id))
    if len(command_games) < 5:
        command_games = random.sample(command_games, len(command_games))
    else:
        command_games = random.sample(command_games, 5)

    if game_reserve_count == 0:
        gr = gr.first()
        if today > gr.greturn_date:
            due_date = today + timedelta(days=4)
            overdue = True
        else:
            due_date = gr.greturn_date + timedelta(days=2)
    elif gr.count() > game_reserve_count:
        grs = gr[game_reserve_count:game_reserve_count+1].get().greturn_date
        due_date = grs + timedelta(days=2)
    else:
        grl = GameReserve.objects.filter(game_id=g_id).last()
        due_date = grl.game_due_date + timedelta(days=16)

    due_date_p = due_date.strftime('%Y.%m.%d')
    if request.method == 'POST':
        g_reserve = GameReserve()
        gg = RentalGame.objects.get(game_id=g_id)
        g_reserve.game_id = gg

        l_check = GameReserve.objects.last()
        if l_check is None:
            g_reserve.game_reserve_id = 1
        else:
            l = GameReserve.objects.latest('game_reserve_id')
            g_reserve.game_reserve_id = l.game_reserve_id + 1

        g_reserve.member_id = i

        g_reserve.game_due_date = due_date

        g_reserve.save()

        game.device_check = 1
        game.save()

        return redirect('/rental/reserve_done')
    else:
        u_already = GameReserve.objects.filter(game_id=g_id, member_id=i).count()
        due_start = due_date - timedelta(days=2)
        due_end = due_date - timedelta(days=1)
        return render(request, 'reserve/game_reserve.html',
                      {'game': game, 'due_start': due_start, 'due_end': due_end, 'due_date': due_date_p, 'authuser': authuser, 'game_reserve_count': game_reserve_count, 'u_already': u_already, 'overdue': overdue, 'command_games': command_games,})


def rental_done(request):
    return render(request, 'rental/rental_done.html')


def reserve_done(request):
    return render(request, 'reserve/reserve_done.html')