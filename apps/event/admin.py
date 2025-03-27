from django.contrib import admin

from apps.event.models import (
    Event,
    Ticket,
    Reservation,
    ReservationItem,
    Payment
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "start_date", "end_date", "is_active", "location", "capacity", "organizer", "available_seats"]
    search_fields = ["name", "description"]
    list_filter = ["is_active", "start_date", "end_date"]
    date_hierarchy = "start_date"
    ordering = ["-start_date"]
    readonly_fields = ["code",  "created_at", "updated_at"]
    exclude = ["deleted_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "organizer",
                    "start_date",
                    "end_date",
                    "is_active",
                    "capacity",
                    "location"
                )
            },
        ),
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["ticket_number", "seat_number", "event", "status"]
    search_fields = ["ticket_number"]
    list_filter = ["status", "event"]
    ordering = ["-created_at"]
    readonly_fields = ["ticket_number", "seat_number", "event", "status", "event", "created_at",  "updated_at"]
    exclude = ["deleted_at"]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "code", "reserved_date", "status", "payment_status"]
    search_fields = ["code"]
    list_filter = ["status", "payment_status", "reserved_date", "event"]
    date_hierarchy = "reserved_date"
    ordering = ["-created_at"]
    readonly_fields = ["code", "user", "event", "status", "payment_status", "reserved_date", "created_at", "updated_at"]
    exclude = ["deleted_at"]

@admin.register(ReservationItem)
class ReservationItemAdmin(admin.ModelAdmin):
    list_display = ["reservation", "ticket"]
    search_fields = ["reservation", "ticket"]
    list_filter = ["reservation", "ticket"]
    ordering = ["-created_at"]
    readonly_fields = ["reservation", "ticket", "created_at", "updated_at"]
    exclude = ["deleted_at"]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["reservation", "amount", "payment_method", "payment_date"]
    search_fields = ["reservation"]
    list_filter = ["reservation", "payment_method"]
    ordering = ["-created_at"]
    readonly_fields = ["reservation", "amount", "payment_method", "payment_date", "created_at", "updated_at"]
    exclude = ["deleted_at"]