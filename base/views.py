from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Room, Topic, Messages, User
from .forms import RoomForm, UserForm, MyUserCreationForm


def login_page(request):
    page = 'login'
    context = {}

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")

    context['page'] = page
    return render(request, 'base/login.html', context=context)


def register_page(request):
    context = {}
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context['form'] = form
    return render(request, 'base/signup.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('login')


def home_page(request):
    context = {}
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:4]
    room_count = rooms.count()
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q))

    context['rooms'] = rooms
    context['topics'] = topics
    context['room_count'] = room_count
    context['room_messages'] = room_messages
    return render(request, 'base/home.html', context=context)


def room_page(request, room_id):
    context = {}
    room = Room.objects.get(id=room_id)
    room_messages = room.messages_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body')
        message = Messages.objects.create(
            user=request.user,
            room=room,
            body=body
        )
        room.participants.add(request.user)
        return redirect('room', room_id=room_id)

    context['room'] = room
    context['room_messages'] = room_messages
    context['participants'] = participants
    return render(request, 'base/room.html', context=context)


def profile_page(request, user_id):
    context = {}
    user = User.objects.get(id=user_id)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.messages_set.all()

    context['user'] = user
    context['rooms'] = rooms
    context['topics'] = topics
    context['room_messages'] = room_messages
    return render(request, 'base/profile.html', context=context)


@login_required(login_url='login')
def edit_profile(request):
    context = {}
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)

    context['form'] = form
    return render(request, 'base/edit_profile.html', context=context)


@login_required(login_url='login')
def create_room(request):
    context = {}
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        name = request.POST.get('name')
        desc = request.POST.get('description')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=name,
            description=desc
        )
        return redirect('home')

    context['form'] = form
    context['topics'] = topics
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def update_room(request, room_id):
    context = {}
    room = Room.objects.get(id=room_id)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        name = request.POST.get('name')
        desc = request.POST.get('description')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.topic = topic
        room.name = name
        room.description = desc
        room.save()
        return redirect('home')

    context['form'] = form
    context['topics'] = topics
    context['room'] = room
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def delete_room(request, room_id):
    context = {}
    room = Room.objects.get(id=room_id)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context['obj'] = room
    return render(request, 'base/delete.html', context=context)


@login_required(login_url='login')
def delete_message(request, msg_id):
    context = {}
    msg = Messages.objects.get(id=msg_id)

    if request.user != msg.user:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        msg.delete()
        return redirect('home')

    context['obj'] = msg
    return render(request, 'base/delete.html', context=context)


def topics_page(request):
    context = {}
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context['topics'] = topics
    return render(request, 'base/topics.html', context=context)


def activity_page(request):
    context = {}
    room_messages = Messages.objects.all()[0:10]

    context['room_messages'] = room_messages
    return render(request, 'base/activity_mobile.html', context=context)
