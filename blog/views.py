#coding=utf-8
from django.shortcuts import render
from blog.models import BlogsPost
from django.template import loader,Context
from django.http import HttpResponse

# Create your views here.
def index(request):
    posts = BlogsPost.objects.all()
    t = loader.get_template("index.html")
    c = Context({'posts':posts})
    return HttpResponse(t.render(c))
