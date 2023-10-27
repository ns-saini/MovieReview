import logging

from django.shortcuts import render
import pika
from django.views.decorators.csrf import csrf_exempt

from .consumers import starter
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.shortcuts import render, HttpResponse
from django.db import connection
import time

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
def index(request):
    return render(request, 'index.html')


def message_queue_send(request):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='ec2-54-204-158-218.compute-1.amazonaws.com',
                                                                   credentials=pika.PlainCredentials('myuser',
                                                                                                     'mypassword')))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    connection.close()
    return render(request, 'index.html')


def message_queue_rcv(request):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='ec2-54-204-158-218.compute-1.amazonaws.com',
                                                                   credentials=pika.PlainCredentials('myuser',
                                                                                                     'mypassword')))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# ----------------------------------------GET--------------------------------
# --------GET BASIC-------------------------

@csrf_exempt
@api_view(['GET'])
def consumers_start(request):
    starter.start()
    return Response()

@csrf_exempt
@api_view(['GET'])
def get_basic(request):
    items = Basic.objects.all()
    serializer = BasicSerializer(items, many=True)
    return Response(serializer.data)


# --------GET NAMES-------------------------

@csrf_exempt
@api_view(['GET'])
def get_names(request):
    items = Names.objects.all()
    serializer = NamesSerializer(items, many=True)
    return Response(serializer.data)


# --------GET PRINCIPAL-------------------------
@csrf_exempt
@api_view(['GET'])
def get_principal(request):
    items = Principal.objects.all()
    serializer = PrincipalSerializer(items, many=True)
    return Response(serializer.data)


# --------GET RATINGS-------------------------
@csrf_exempt
@api_view(['GET'])
def get_ratings(request):
    items = Ratings.objects.all()
    serializer = RatingsSerializer(items, many=True)
    return Response(serializer.data)


# --------GET RATINGS-------------------------
@csrf_exempt
@api_view(['GET'])
def get_titletoname(request):
    items = TitleToName.objects.all()
    serializer = TitleToNameSerializer(items, many=True)
    return Response(serializer.data)


# ------------------------------------POST---------------------------

@csrf_exempt
@api_view(['POST'])
def add_basic(request):
    serializer = BasicSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_name(request):
    serializer = NamesSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_principal(request):
    serializer = PrincipalSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_titletoname(request):
    serializer = TitleToNameSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_ratings(request):
    serializer = RatingsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@csrf_exempt
def search_names(request):
    # print("Search Names.......................")
    return render(request, 'search_names.html')


@csrf_exempt
def display_names(request):
    start_time = time.time()
    if request.method == 'POST':
        name_val = request.POST['name']
        logging.info("Name: %s", name_val)
        cache_hit = cache.get(name_val)
        logging.info("Cache Hit: %s", cache_hit)
        # CACHE LOGIC START
        if cache_hit:
            print("Getting From Cache, FASTTT")
            data = cache_hit
        else:
            print("GETTING FROM DB......SLOWWWWW")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT  id, name, birth_year, death_year, primary_profession from names where name = " + "\'" + name_val + "\'")
            data = cursor.fetchall()
            print("Data Is")
            logging.info('data', data)
            cache.set(name_val, data)
            cursor.close()
        print("--- %s seconds ---" % (time.time() - start_time))
        time_execution = time.time() - start_time
        time_execution = round(time_execution, 3)
        return render(request, 'display_names.html', {'emps': data,'time':time_execution})
    elif request.method == 'GET':
        return render(request, 'search_names.html')
    else:
        return HttpResponse('An Exception Occurred')


# -------------------------------------------------------------

@csrf_exempt
def search_movie(request):
    # print("Search Names.......................")
    return render(request, 'search_movie.html')


@csrf_exempt
def display_movie_details(request):
    # print("Printing Names Below ")
    start_time = time.time()

    if request.method == 'POST':
        # print("Inside Post")
        title = request.POST['primary_title']

        # CACHE LOGIC START
        if cache.get(title):
            print("Getting From Cache, FASTTT")
            data = cache.get(title)
        else:
            print("GETTING FROM DB......SLOWWWWW")

            cursor = connection.cursor()
            cursor.execute(
                "SELECT b.title_id, b.title, r.AVG_RATING, r.VOTES from ratings r , basic b WHERE r.title_id  = "
                "b.title_id and b.title like " + "\'%" + title + "%\'")

            # Fetch Data according to Query

            data = cursor.fetchall()
            cache.set(title, data)

            # print(data)

            cursor.close()

        time_execution = time.time() - start_time
        time_execution = round(time_execution, 3)

        return render(request, 'display_movie_details.html', {'emps': data,'time':time_execution})

    elif request.method == 'GET':
        return render(request, 'search_movie.html')
    else:
        return HttpResponse('An Exception Occurred')
