from apps.core.permissions import AbstractAccessPolicy


class EventAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class TicketAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class ReservationAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class PaymentAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset
