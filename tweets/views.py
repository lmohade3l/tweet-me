from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404 , JsonResponse, HttpResponseRedirect
import random
from django.utils.http import is_safe_url
from django.conf import settings
from .forms import TweetForm
from .models import Tweet
from .serials import TweetSerializer , TweetActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.

def home_view(request , *args , **kwargs) :
    # return HttpResponse('<h1>Hello World!</h1>')
    return render(request , 'pages/home.html' , context={} , status=200)


@api_view(['POST']) #http method that client has to send === POST
# @authentication_classes([SessionAuthentication]) #done by defaullt?
@permission_classes([IsAuthenticated])
def tweet_create_view(request , *args , **kwargs ):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data , status=201)
    return Response({} , status=400)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({} , status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data , status=200)


@api_view(['DELETE' , 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({} , status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message':'you cannot delete this tweet!'} , status=404)
    obj = qs.first()
    obj.delete()
    return Response({'message':'tweet deleted'} , status=200)


@api_view(['DELETE' , 'POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
        id is required
        actions: like , unlike, retweet
    '''
    serializer = TweetActionSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')

        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({} , status=404)
        obj = qs.first()
        if action=='like':
            obj.likes.add(request.user)
        elif action=='unlike':
            obj.likes.remove(request.user)
        elif action=='retweet':
            pass

    return Response({'message':'tweet deleted'} , status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs , many=True)
    
    return Response(serializer.data)


def tweet_create_view_pure_django(request , *args , **kwargs ):
    '''
    REST API create View
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax:
            return JsonResponse({} , status=401)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)

        obj.user = request.user or None #annon user

        obj.save()

        if request.is_ajax:
            return JsonResponse(obj.serialize() , status=201)
            
        if next_url != None and is_safe_url(next_url , ALLOWED_HOSTS):
            return redirect(next_url)
        
        form = TweetForm()

    if form.errors:
        if request.is_ajax:
            return JsonResponse(form.errors , status=400)
        
    return render(request , 'components/form.html' , context={'form':form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    # tweets_list = [{'id':x.id , 'content':x.content , 'likes':random.randint(0,100)} for x in qs]
    tweets_list = [x.serialize() for x in qs]
    data = {
        'is_user' : False,
        'response': tweets_list
    }
    return JsonResponse(data)

# def tweet_detail_view(request ,tweet_id, *args , **kwargs) :
#     try :
#         obj = Tweet.objects.get(id=tweet_id)
#         return HttpResponse(f"<h1>this is a xxxtweet with id= {tweet_id} {obj.content}</h1>")
#     except :
#         raise Http404

#REST API view, return json data to consume by js
def tweet_detail_view_pure_django(request ,tweet_id, *args , **kwargs) :
    data = {
        'id' : tweet_id,
    }
    status = 200
    try :
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except :
        data['message'] = 'not found!'
        status = 404
    
    
    return JsonResponse(data , status=status)