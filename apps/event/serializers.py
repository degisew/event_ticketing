import logging
from rest_framework import serializers
from apps.account.serializers import UserResponseSerializer
from apps.core.serializers import (
    DataLookupResponseSerializer,
    DynamicFieldsModelSerializer,
)
from apps.core.exceptions import SerializationError
from apps.event.models import Event, Ticket, Reservation, TicketType, Transaction
from apps.core.utils import generate_unique_code
from apps.event.services import TransactionService, ReservationService

logger = logging.getLogger(__name__)


class EventResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "code",
            "description",
            "start_date",
            "end_date",
            "is_active",
            "capacity",
            "location",
            "created_at",
            "updated_at",
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "is_active",
            "capacity",
            "location",
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        code = generate_unique_code("EVT", "")
        organizer = self.context["request"].user
        validated_data["organizer"] = organizer
        validated_data["code"] = code

        return super().create(validated_data)

    def to_representation(self, instance):
        return EventResponseSerializer(
            instance, context=self.context
        ).to_representation(instance)


class TicketTypeResponseSerializer(DynamicFieldsModelSerializer):
    category = DataLookupResponseSerializer(fields=["name", "remark"])

    class Meta:
        model = TicketType
        fields = [
            "id",
            "category",
            "event",
            "price",
            "total_tickets",
            "available_tickets",
        ]


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ["category", "event", "price", "total_tickets"]

    def to_representation(self, instance):
        return TicketTypeResponseSerializer(
            instance, context=self.context
        ).to_representation(instance)


class ReservationResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(fields=["email"])
    ticket_type = TicketTypeResponseSerializer()
    ticket_type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "ticket_type",
            "reserved_date",
            "status",
            "payment_status",
            "created_at",
            "updated_at",
        ]

    # * Doing all this below to avoid nested dict response format
    # * Since we already preloaded, it doesn't add N + 1 query
    def get_status(self, obj):
        return obj.status.name if obj.status else None

    def get_payment_status(self, obj):
        return obj.payment_status.name if obj.payment_status else None

    def get_ticket_type(self, obj):
        return obj.ticket_type.category.name


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "event",
            "ticket_type",
            "ticket_quantity",
        ]

    def validate_ticket_quantity(self, value):
        """Validate ticket quantity is positive and within limits"""
        if value <= 0:
            raise serializers.ValidationError("Ticket quantity must be positive")

        # TODO: We assume 10 ticket per reservation. refine it.
        if value > 10:
            raise serializers.ValidationError("Maximum 10 tickets per reservation")

        return value

    def validate(self, attrs):
        try:
            event = attrs.get("event")

            if not event:
                raise serializers.ValidationError("Event is required")

            if not event.is_active:
                raise serializers.ValidationError("Event is not active")

            # Validate ticket type belongs to the given event
            ticket_type = attrs.get("ticket_type")
            if ticket_type and ticket_type.event_id != event.id:
                raise serializers.ValidationError(
                    "Ticket type does not belong to this event"
                )

            return attrs

        except Exception as e:
            logger.error(f"Validation error in ReservationSerializer: {str(e)}")

            raise serializers.ValidationError("Invalid reservation data")

    def create(self, validated_data) -> Reservation:
        user = self.context["request"].user
        validated_data["user"] = user

        logger.info(
            f"Creating reservation for user {user.id}, event {validated_data['event'].id}"
        )

        return ReservationService.create_reservation(validated_data)

    def to_representation(self, instance):
        try:
            return ReservationResponseSerializer(
                instance, context=self.context
            ).to_representation(instance)
        except Exception as e:
            logger.error(f"Error in to_representation: {str(e)}", exc_info=True)
            raise SerializationError("Unable to fully serialize reservation details.")


class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "reservation",
            "ticket_number",
            "status",
            "created_at",
            "updated_at",
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["reservation"]

    def to_representation(self, instance):
        return TicketResponseSerializer(
            instance, context=self.context
        ).to_representation(instance)


class TransactionResponseSerializer(serializers.ModelSerializer):
    # reservation = ReservationSerializer()
    event = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            # "reservation",
            "event",
            "transaction_date",
            "amount",
            "payment_method",
            "created_at",
            "updated_at",
        ]

    def get_event(self, obj):
        return obj.reservation.event.name


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["reservation", "payment_method"]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return TransactionService.transaction_handler(validated_data)

    def to_representation(self, instance):
        return TransactionResponseSerializer(
            instance, context=self.context
        ).to_representation(instance)
