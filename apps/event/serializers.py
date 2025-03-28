from rest_framework import serializers
from apps.account.serializers import UserSerializer
from apps.event.models import Event, Ticket, Reservation, Payment
from apps.core.utils import generate_unique_code
from apps.event.services import PaymentService, ReservationService


class EventResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'code',
            'organizer',
            'description',
            'start_date',
            'ticket_price',
            'end_date',
            'is_active',
            'capacity',
            'available_seats',
            'location',
            'created_at',
            'updated_at'
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'start_date',
            'end_date',
            'ticket_price',
            'is_active',
            'capacity',
            'location'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        code = generate_unique_code("EVT", "")
        organizer = self.context['request'].user
        validated_data['organizer'] = organizer
        validated_data['code'] = code
        
        return super().create(validated_data)

    def to_representation(self, instance):
        return EventResponseSerializer(
            instance,
            context=self.context
        ).to_representation(instance)


class ReservationResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    event = EventSerializer()

    class Meta:
        model = Reservation
        fields = [
            'id',
            'user',
            'event',
            'reserved_date',
            'payment_status',
            'created_at',
            'updated_at'
        ]


class ReservationSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = [
            'event',
            'reserved_date',
            'quantity'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data) -> Reservation:
        user = self.context['request'].user
        validated_data['user'] = user

        try:
            return ReservationService.create_reservation(validated_data)
        except Exception as e:
            raise e

    def to_representation(self, instance):
        return ReservationResponseSerializer(
            instance,
            context=self.context
        ).to_representation(instance)


class TicketResponseSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'event',
            'ticket_number',
            'seat_number',
            'status',
            'created_at',
            'updated_at'
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'event',
            'seat_number'
        ]

    def to_representation(self, instance):
        return TicketResponseSerializer(
            instance,
            context=self.context
        ).to_representation(instance)


class PaymentResponseSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()

    class Meta:
        model = Payment
        fields = [
            'id',
            'reservation',
            'payment_date',
            'amount',
            'payment_method',
            'created_at',
            'updated_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'reservation',
            'payment_method'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            return PaymentService.process_payment(user, validated_data)
        except Exception as e:
            raise e

    def to_representation(self, instance):
        return PaymentResponseSerializer(
            instance,
            context=self.context
        ).to_representation(instance)
