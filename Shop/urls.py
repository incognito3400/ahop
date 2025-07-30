from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve

print('olofmeister is the best player in the world')

# Відповідає за маршрутизацію запитів до відповідних view-функцій.

urlpatterns = [
    # Адмін-панель Django
    path('admin/', admin.site.urls),

    # Головна сторінка
    path('', views.main_page, name='main_page'),

    # Сторінка бронювання кімнати за ID
    path('book_room/<int:room_id>/', views.book_room, name='book_room'),

    # Сторінка зі списком доступних кімнат
    path('available_rooms/', views.available_rooms, name='available_rooms'),

    # Сторінка з бронюваннями користувача
    path('my_bookings/', views.my_bookings, name='my_bookings'),

    # Вихід з акаунту
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Вхід та реєстрація (використовує стандартні URL Django auth)
    path('accounts/', include('django.contrib.auth.urls')),

    # Сторінка реєстрації нового користувача
    path('register/', views.register, name='register'),

    # Додавання нової кімнати (для персоналу)
    path('add_room/', views.add_room, name='add_room'),

    # Редагування кімнати за ID (для персоналу)
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),

    # Видалення кімнати за ID (для персоналу)
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),

    # Скасування бронювання за ID
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Видалення бронювання за ID
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),

    # Деталі кімнати за ID
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
]

# Обробка медіа-файлів у продакшн-режимі
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Додавання статичних та медіа URL для розробки
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
