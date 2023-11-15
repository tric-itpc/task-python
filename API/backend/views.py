from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from backend.models import Service, ServiceState
from backend.serializers import ServiceSerializer, ServiceStateSerializer


class ServiceView(APIView):
    """
    Класс для работы с данными сервиса
    """

    # получение сервиса
    def get(self, request, *args, **kwargs):
        if {"id", "key"}.issubset(request.data):
            service = Service.objects.filter(**request.data)
            if service:
                return Response(
                    ServiceSerializer(service[0]).data,
                    status=200,
                )
            return Response(
                {"Status": False, "Error": "Сервиса не существует"}, status=404
            )
        return Response({"Status": False, "Errors": "Не указан id сервиса"}, status=200)

    # создание нового сервиса
    def post(self, request, *args, **kwargs):
        if not Service.objects.filter(**request.data):
            if {"name"}.issubset(request.data):
                service_serializer = ServiceSerializer(data=request.data)
                if service_serializer.is_valid():
                    try:
                        service = service_serializer.save()
                    except IntegrityError as error:
                        return Response(
                            {"Status": False, "Errors": str(error)}, status=200
                        )
                    else:
                        return Response(
                            {
                                "status": True,
                                "id": service.id,
                                "key": service.key,
                                "created_at": service.created_at,
                            },
                            status=201,
                        )
                return Response(
                    {"Status": False, "Errors": service_serializer.errors}, status=200
                )
            return Response(
                {"Status": False, "Errors": "Не указаны все необходимые данные (name)"},
                status=200,
            )
        return Response({"Status": False, "Error": "Сервис уже существует"}, status=200)

    # изменение данных сервиса
    def patch(self, request, *args, **kwargs):
        if {"id", "key"}.issubset(request.data):
            service = Service.objects.filter(
                id=request.data["id"], key=request.data["key"]
            )
            if service:
                service_serializer = ServiceSerializer(
                    service[0], data=request.data, partial=True
                )
                if service_serializer.is_valid():
                    try:
                        service_serializer.save()
                    except IntegrityError as error:
                        return Response(
                            {"Status": False, "Errors": str(error)}, status=200
                        )
                    else:
                        return Response(
                            {"Status": True, "info": "Изменения внесены"}, status=201
                        )
                return Response(
                    {"Status": False, "Errors": service_serializer.errors}, status=200
                )
            return Response(
                {"Status": False, "Error": "Сервиса не существует"}, status=404
            )
        return Response({"Status": False, "Errors": "Не указан id сервиса"}, status=200)


class ServiceStateView(APIView):
    """
    Класс для работы с состоянием сервиса
    """

    # получение актуального состояния сервиса
    def get(self, request, *args, **kwargs):
        if {"id", "key"}.issubset(request.data):
            if Service.objects.filter(**request.data):
                state = ServiceState.objects.filter(
                    service=request.data["id"], relevance=True
                )
                if state:
                    return Response(
                        ServiceStateSerializer(state[0]).data,
                        status=200,
                    )
                return Response(
                    {"Status": False, "Error": "Актуальных данных нет"}, status=404
                )
            return Response({"Status": False, "Errors": "Сервис не найден"}, status=404)
        return Response({"Status": False, "Errors": "Не указан id сервиса"}, status=200)

    # создание новой записи состояния сервиса
    def post(self, request, *args, **kwargs):
        if {"id", "key", "state", "description"}.issubset(request.data):
            if Service.objects.filter(id=request.data["id"], key=request.data["key"]):
                state_serializer = ServiceStateSerializer(
                    data={
                        "service": request.data["id"],
                        "state": request.data["state"],
                        "description": request.data["description"],
                    }
                )
                if state_serializer.is_valid():
                    try:
                        state = state_serializer.save()
                    except IntegrityError as error:
                        return Response(
                            {"Status": False, "Errors": str(error)}, status=200
                        )
                    else:
                        ServiceState.objects.filter(service=request.data["id"]).exclude(
                            id=state.id
                        ).update(relevance=False)
                        return Response(
                            {
                                "status": True,
                                "id_recording": state.id,
                            },
                            status=201,
                        )
                return Response(
                    {"Status": False, "Errors": state_serializer.errors}, status=200
                )
            return Response({"Status": False, "Errors": "Сервис не найден"}, status=404)
        return Response({"Status": False, "Errors": "Не указан id сервиса"}, status=200)


class AllRecordingView(ModelViewSet):
    """
    Класс для работы со всей историей записей статусов состояния сервиса
    """

    queryset = ServiceState.objects.filter(service__is_active=True)
    serializer_class = ServiceStateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["service"]
    pagination_class = LimitOffsetPagination
    http_method_names = ["get"]


@api_view(["GET"])
def get_all_service_view(request, *args, **kwargs):
    service = Service.objects.filter(is_active=True)
    if service:
        return Response(
            {
                "Status": True,
                "Info": {
                    el.id: ServiceState.objects.get(service=el.id, relevance=True).state
                    for el in service
                },
            },
            status=200,
        )
    return Response({"Status": False, "Error": "Отсутсвуют сервисы"}, status=404)


# для получения данных работы сервиса (в разработке)
@api_view(["GET"])
def get_info_stateservice_view(request, *args, **kwargs):
    if {"id", "after", "till"}.issubset(request.data):
        ServiceState.objects.filter(datetime__gte=request.data["after"]).filter(
            datetime__lte=request.data["till"]
        )
        pass
    return Response(
        {"Status": False, "Errors": "Не указан необходимые данные (id, after, till)"},
        status=200,
    )
