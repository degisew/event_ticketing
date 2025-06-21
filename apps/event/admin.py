from django.contrib import admin

from apps.event.models import (
    Event,
    Ticket,
    Reservation,
    TicketType,
    Transaction
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "start_date", "end_date",
                    "is_active", "location", "capacity", "organizer"]
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
    list_display = ["ticket_number", "reservation", "status", "created_at"]
    search_fields = ["ticket_number"]
    list_filter = ["status", "reservation"]
    ordering = ["-created_at"]
    readonly_fields = ["ticket_number", "status", "reservation", "created_at", "updated_at"]
    exclude = ["deleted_at"]


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ["category__name", "event", "price", "total_tickets"]
    search_fields = ["event"]
    list_filter = ["event__name"]
    readonly_fields = ["available_tickets"]
    ordering = ["-created_at"]
    exclude = ["deleted_at"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["code", "user", "event", "ticket_type__category__name",
                    "reserved_date", "status", "payment_status"]
    search_fields = ["code"]
    list_filter = ["status", "payment_status", "reserved_date", "event"]
    date_hierarchy = "reserved_date"
    ordering = ["-created_at"]
    readonly_fields = ["code", "user", "event", "status", "payment_status",
                       "reserved_date", "created_at", "updated_at"]
    exclude = ["deleted_at"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["reservation", "amount", "payment_method", "transaction_date"]
    search_fields = ["reservation"]
    list_filter = ["reservation", "payment_method"]
    ordering = ["-created_at"]
    readonly_fields = ["reservation", "amount", "payment_method",
                       "transaction_date", "created_at", "updated_at"]
    exclude = ["deleted_at"]
