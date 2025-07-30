from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking, RoomPhoto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.db.models import Q
from .forms import RoomForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST


@staff_member_required
def edit_room(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        files = request.FILES.getlist('images')
        if form.is_valid():
            room = form.save()
            for f in files:
                RoomPhoto.objects.create(room=room, image=f)
            return redirect('available_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'add_room.html', {'form': form, 'edit_mode': True, 'room': room})


@staff_member_required
@require_POST
def delete_room(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect('available_rooms')


def available_rooms(request):
    
    rooms = Room.objects.all()
    return render(request, 'available_rooms.html', {'rooms': rooms})


@staff_member_required
def add_room(request):
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            room = form.save()
            for f in files:
                RoomPhoto.objects.create(room=room, image=f)
            return redirect('available_rooms')
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})


@login_required
def book_room(request, room_id):
    
    error_message = None
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        error_message = "Room not found."
        return render(request, 'book_room.html', {'error_message': error_message})

    if request.method == 'POST':
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')

        check_in_date = parse_date(check_in_date_str)
        check_out_date = parse_date(check_out_date_str)

        if not check_in_date or not check_out_date:
            error_message = "Invalid date format."
        elif check_in_date >= check_out_date:
            error_message = "Check-out date must be after check-in date."
        else:
            overlapping_bookings = Booking.objects.filter(
                room=room,
                is_confirmed=True
            ).filter(
                Q(check_in_date__lt=check_out_date) & Q(check_out_date__gt=check_in_date)
            )
            if overlapping_bookings.exists():
                error_message = "The room is already booked for the selected dates."
            else:
                booking = Booking.objects.create(
                    user=request.user,
                    room=room,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    is_confirmed=True
                )
                room.is_available = False
                room.save()
                return redirect('my_bookings')

    return render(request, 'book_room.html', {'room': room, 'error_message': error_message})


@login_required
def my_bookings(request):
    
    bookings = Booking.objects.filter(user=request.user, is_confirmed=True)
    return render(request, 'my_bookings.html', {'bookings': bookings})


def register(request):
   
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def main_page(request):
    
    from .models import Room
    rooms = Room.objects.prefetch_related('photos').all()
    return render(request, 'main.html', {'rooms': rooms})


@login_required
@require_POST
def cancel_booking(request, booking_id):
   
    booking = Booking.objects.filter(id=booking_id, user=request.user, is_confirmed=True).first()
    if booking:
        if request.POST.get('delete') == 'true':
            booking.room.is_available = True
            booking.room.save()
            booking.delete()
        else:
            booking.is_confirmed = False
            booking.save()
            booking.room.is_available = True
            booking.room.save()
    return redirect('my_bookings')


@login_required
@require_POST
def delete_booking(request, booking_id):
   
    booking = Booking.objects.filter(id=booking_id, user=request.user).first()
    if booking:
        booking.delete()
    return redirect('my_bookings')


def room_detail(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)
    photos = room.photos.all()
    return render(request, 'room_detail.html', {'room': room, 'photos': photos})


def page_404(request, exception):
   
    return render(request, '404.html', status=404)

