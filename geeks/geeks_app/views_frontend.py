from .mixins import *
from .models import *
from django.shortcuts import render_to_response,get_object_or_404
from django.apps import apps
from datetime import datetime, timedelta
from urllib.parse import quote_plus

class Index(FrontendMixin,TemplateView):
    template_name = "geeks_app/frontend_geeks/index.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        if Post.objects.filter(deleted_at__isnull=True).count() > 0:
            context['Allpost'] = Post.objects.filter(publish=True, deleted_at__isnull=True).order_by('-created_at')
            context['mostrecentpost'] = Post.objects.filter(publish=True, deleted_at__isnull=True).order_by('-created_at')[:10]
        else:
            context = []
        
        return context


class FrontendPostDetail(FrontendMixin,DetailView):

    template_name = 'geeks_app/frontend_geeks/detail.html'
    context_object_name = 'post_object'
    model = Post 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Post.objects.filter(deleted_at__isnull=True).count() > 0:
            context['mostrecentpost'] = Post.objects.filter(publish=True, deleted_at__isnull=True).order_by('-created_at')[:10]
        else:
            context = []
        return context 


class PythonHome(FrontendMixin,TemplateView):
    template_name = 'geeks_app/frontend_geeks/python.html'
    # context_object_name = 'post_object'
    # model = Post
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        if Post.objects.filter(deleted_at__isnull=True).count() > 0:
            python_id = Category.objects.get(name='Python').id
            context["python_object"] = Post.objects.filter(category=python_id, publish=True, deleted_at__isnull=True)[:10]
            context['mostrecentpost'] = Post.objects.filter(publish=True, deleted_at__isnull=True).order_by('-created_at')[:10]
        else:
            context = []
        return context
    

class MachineLearningHome(FrontendMixin,TemplateView):
    template_name = 'geeks_app/frontend_geeks/machine_learning.html'
    # context_object_name = 'post_object'
    # model = Post
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        if Post.objects.filter(deleted_at__isnull=True).count() > 0:
            machinelearning_id = Category.objects.get(name='Machine Learning').id
            context["machinelearning_object"] = Post.objects.filter(category=machinelearning_id, publish=True, deleted_at__isnull=True)[:10]
            context['mostrecentpost'] = Post.objects.filter(publish=True, deleted_at__isnull=True).order_by('-created_at')[:10]
        else:
            context = []
        return context


class ChallengeHome(FrontendMixin,TemplateView):
    template_name = 'geeks_app/frontend_geeks/challenge.html'
    # context_object_name = 'post_object'
    # model = Post
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        if Post.objects.filter(deleted_at__isnull=True).count() > 0:
            challenge_id = Category.objects.get(name='Challenge').id
            context["challenge_object"] = Post.objects.filter(category=challenge_id, publish=True, deleted_at__isnull=True)[:10]
            context['mostrecentpost'] = Post.objects.filter(publish=True, deleted_at__isnull=True).order_by('-created_at')[:10]
        else:
            context = []
        return context
