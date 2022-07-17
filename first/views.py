from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Store
from .seriaizers import StoreSerializer


@api_view(http_method_names=['GET'])
def hello_world(request):
    return_dict = {'message': 'Hello World'}
    return Response(return_dict)


@api_view(http_method_names=['GET'])
def my_name(request):
    name = request.query_params
    return Response({'name': name['name']})


@api_view(http_method_names=['GET'])
def today(request):
    now = datetime.now()
    return_dict = {'date': now.strftime("%d/%m/%Y"), 'year': now.strftime("%Y"), 'month': now.strftime("%m"),
                   'day': now.strftime("%d")}
    return Response(return_dict)


@api_view(http_method_names=['POST'])
def calculator(request):
    action = request.data['action']
    number1 = request.data['number1']
    number2 = request.data['number2']
    if action in ['minus', 'plus', 'divide', 'multiply']:
        if action == 'minus':
            res = number1 - number2
            return Response({'res': res})
        elif action == 'plus':
            res = number1 + number2
            return Response({'res': res})
        elif action == 'multiply':
            res = number1 * number2
            return Response({'res': res})
        elif action == 'divide':
            if number2 != 0:
                res = number1 / number2
                return Response({'res': res})
            else:
                return Response(['Деление на ноль недопустимо'], status=HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(['Не верный формат данных'], status=HTTP_422_UNPROCESSABLE_ENTITY)


class StoreApiView(APIView):
    def get(self, request, format=None):
        result = Store.objects.all()
        serializer = StoreSerializer(result, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED, data=serializer.data)


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(**{'owner': self.request.user})

    @action(http_method_names=['POST'], detail=True)
    def mark_as_active(self, request, pk=None):
        store = self.get_object()
        if store.status == 'deactivated':
            store.status = 'active'
            store.save()
        serializer = self.get_serializer(store)
        return Response(serializer.data)

    @action(http_method_names=['POST'], detail=True)
    def mark_as_deactivated(self, request, pk=None):
        store = self.get_object()
        if store.status == 'active':
            store.status = 'deactivated'
            store.save()
        serializer = self.get_serializer(store)
        return Response(serializer.data)



class StoreUserViewSet(ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Store.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(**{'owner': self.request.user})


class AdminStoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title']

    @action(http_method_names=['POST'], detail=True)
    def mark_as_active(self, request, pk=None):
        store = self.get_object()
        if store.status == 'in_review':
            store.status = 'active'
            store.save()
        serializer = self.get_serializer(store)
        return Response(serializer.data)