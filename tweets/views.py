from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404 , JsonResponse, HttpResponseRedirect
import random
from django.utils.http import is_safe_url
from django.conf import settings
from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.

def home_view(request , *args , **kwargs) :
    # return HttpResponse('<h1>Hello World!</h1>')
    return render(request , 'pages/home.html' , context={} , status=200)

def tweet_create_view(request , *args , **kwargs ):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url , ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request , 'components/form.html' , context={'form':form})

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