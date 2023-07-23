from django.shortcuts import render
from django.http import HttpResponse, Http404 , JsonResponse
import random

from .forms import TweetForm
from .models import Tweet

# Create your views here.

def home_view(request , *args , **kwargs) :
    # return HttpResponse('<h1>Hello World!</h1>')
    return render(request , 'pages/home.html' , context={} , status=200)

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{'id':x.id , 'content':x.content , 'likes':random.randint(0,100)} for x in qs]
    data = {
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
def tweet_detail_view(request ,tweet_id, *args , **kwargs) :
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