from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

class CustomUserAdmin(BaseUserAdmin):
   
    def has_add_permission(self, request):
        
        return request.user.is_superuser and request.user.username == 'nikl32Admin'

    def has_change_permission(self, request, obj=None):
        
        return request.user.is_superuser and request.user.username == 'nikl32Admin'

    def has_delete_permission(self, request, obj=None):
        
        return request.user.is_superuser and request.user.username == 'nikl32Admin'


# Реєстрація моделей Booking та Room з кастомним адміністратором
from .models import Booking, Room


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
   
    list_display = ("id", "user", "room", "check_in_date", "check_out_date", "is_confirmed")
    list_filter = ("is_confirmed", "room", "user")
    search_fields = ("user__username", "room__number")
    actions = ["cancel_booking_action"]

    @admin.action(description="Cancel selected bookings")
    def cancel_booking_action(self, request, queryset):
       
        updated = queryset.update(is_confirmed=False)
        for booking in queryset:
            booking.room.is_available = True
            booking.room.save()
        self.message_user(request, f"{updated} booking(s) cancelled.")

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
   
    list_display = ("number", "type", "price", "is_available")
    list_editable = ("is_available",)
    search_fields = ("number", "type")

    def save_model(self, request, lox, form, change):
       
        if "is_available" in form.changed_data and lox.is_available:
            Booking.objects.filter(room=lox, is_confirmed=True).update(is_confirmed=False)
        super().save_model(request, lox, form, change)
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
