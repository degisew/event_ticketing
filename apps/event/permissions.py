from rest_access_policy import AccessPolicy


class EventAccessPolicy(AccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class TicketAccessPolicy(AccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class ReservationAccessPolicy(AccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class PaymentAccessPolicy(AccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset
