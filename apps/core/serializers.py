from apps.core.models import DataLookup, SystemSetting
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DataLookupResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DataLookup
        fields = [
            "id",
            "type",
            "name",
            "value",
            "category",
            "is_default",
            "description",
            "remark",
            "index",
            "created_at",
            "updated_at",
        ]


class DataLookupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataLookup
        fields = ("type",)


class SystemSettingResponseSerializer(serializers.ModelSerializer):
    is_resetable = serializers.SerializerMethodField()

    class Meta:
        model = SystemSetting
        fields = [
            "id",
            "name",
            "key",
            "current_value",
            "is_resetable",
            "created_at",
            "updated_at",
        ]

    def get_is_resetable(self, instance):
        return instance.default_value != instance.current_value


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = [
            "id",
            "name",
            "key",
            "current_value",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        return SystemSettingResponseSerializer(instance).to_representation(instance)


class ResetSystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = []

    def validate(self, attrs):
        if self.instance.default_value == self.instance.current_value:
            raise serializers.ValidationError(
                "The setting is already at default value."
            )
        return attrs

    def to_representation(self, instance):
        return SystemSettingResponseSerializer(instance).to_representation(instance)
