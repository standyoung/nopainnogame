from django.db.models import Count
from django.shortcuts import render


# Create your views here.
from board.models import Post
from rental.models import *


def home(request):
    authuser = request.session.get('authUser')
    dr_day = None
    gr_day = None
    device_rental = None
    game_rental = None
    notice_no = 0
    if authuser:
        user = User.objects.get(member_id=authuser['member_id'])
        today = datetime.now().date()
        device_rental = DeviceRental.objects.filter(member_id=user, overdue=None)
        game_rental = GameRental.objects.filter(member_id=user, overdue=None)
        if device_rental.count() > 0:
            for dr in device_rental:
                if today >= (dr.dreturn_date - timedelta(days=2)) and today < dr.dreturn_date:
                    dr_day = 0
                    notice_no = notice_no + 1
                elif today >= dr.dreturn_date:
                    dr_day = today - dr.dreturn_date
                    dr_day = dr_day.days + 1
                    notice_no = notice_no + 1
                    # d_reserve = DeviceReserve.objects.filter(device_id=dr.device_id)
                    # if d_reserve.count() > 0:
                    #     for drr in d_reserve:
                    #         drr.device_due_date = drr.device_due_date + timedelta(days=r_day)
        if game_rental.count() > 0:
            for gr in game_rental:
                if today >= (gr.greturn_date - timedelta(days=2)) and today < gr.greturn_date:
                    gr_day = 0
                    notice_no = notice_no + 1
                elif today >= gr.greturn_date:
                    gr_day = today - gr.greturn_date
                    gr_day = gr_day.days + 1
                    notice_no = notice_no + 1

    devices = RentalDevice.objects.annotate(d_likes=Count('device_like')).order_by('-d_likes')
    devices = devices[:4]

    games = RentalGame.objects.annotate(g_likes=Count('game_like')).order_by('-g_likes')
    games = games[:4]

    posts = Post.objects.all()
    posts = posts[:7]

    game_v = RentalGame.objects.filter(game_video__isnull=False).values_list('game_video', flat=True)

    return render(request, 'home/home.html', {'dr_day': dr_day, 'device_rental': device_rental, 'gr_day': gr_day, 'game_rental': game_rental, 'notice_no': notice_no, 'devices':devices, 'games': games, 'posts': posts, 'game_v': game_v})


def how_to(request):
    return render(request, 'home/how_to.html')


def how_to_clean(request):
    return render(request, 'home/how_to_clean.html')


def how_to_pick(request):
    return render(request, 'home/how_to_pick.html')