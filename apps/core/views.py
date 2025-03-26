from http import HTTPMethod
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny

from apps.core.models import DataLookup
from apps.core.permissions import (
    DataLookupAccessPolicy,
    SystemSettingAccessPolicy,
)
from apps.core.serializers import (
    DataLookupSerializer,
    DataLookupTypeSerializer,
    SystemSettingSerializer,
    SystemSettingResponseSerializer,
    ResetSystemSettingSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import SystemSetting


class AbstractModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Soft delete data records.
    #     """

    #     instance = self.get_object()
    #     instance.object_state = DataLookup.objects.get(
    #         value=ObjectStateType.DELETED.value
    #     )
    #     instance.deleted_at = timezone.now()
    #     instance.save()

    #     return Response(status=status.HTTP_204_NO_CONTENT)


class DataLookupViewSet(AbstractModelViewSet):
    http_method_names = ['get']
    permission_classes = [AllowAny]
    queryset = DataLookup.objects.all()
    serializer_class = DataLookupSerializer


class DataLookupTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [DataLookupAccessPolicy]
    pagination_class = None
    queryset = DataLookup.objects.all().distinct("type").order_by("type")
    serializer_class = DataLookupTypeSerializer


class SystemSettingViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [SystemSettingAccessPolicy]
    queryset = SystemSetting.objects.all()
    http_method_names = ["get", "post", "patch"]
    serializer_class = SystemSettingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    @action(
        url_path="reset",
        detail=True,
        methods=[HTTPMethod.PATCH],
        serializer_class=ResetSystemSettingSerializer,
    )
    def reset(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            instance.current_value = instance.default_value
            instance.save()
            return Response(
                SystemSettingResponseSerializer(instance).data,
                status=status.HTTP_200_OK,
            )
