from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Service
from .serializers import ServiceSerializer


class ServiceListApiView(GenericAPIView):

    # adding permissions to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get(self, request, *args, **kwargs):
        """ Return a list of all existing Services. """
        services = Service.objects.order_by('slug_name', '-created_at').distinct('slug_name')
        serializer = ServiceSerializer(services, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Create a new Service instance. """
        data = {
            'name': request.data.get('name'),
            'state': request.data.get('state'),
            'description': request.data.get('description')
        }
        serializer = ServiceSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailsApiView(GenericAPIView):
    # adding permissions to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get(self, request, *, slug_name):
        """ Return specific Service details with history of states, current SLA and total downtime. """
        services = Service.objects.filter(slug_name=slug_name).order_by('-created_at')
        if len(services) == 0:
            raise Http404()
        serializer = ServiceSerializer(services, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
