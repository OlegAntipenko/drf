from datetime import datetime

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

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
                return Response(['Деление на ноль недопустимо'], status=HTTP_406_NOT_ACCEPTABLE )
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
