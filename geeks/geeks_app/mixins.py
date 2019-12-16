from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.core import serializers
from django.utils import timezone
from django.views.generic import (
    TemplateView, FormView, UpdateView, ListView, CreateView, DetailView, DeleteView)
from django.contrib.auth import authenticate, login, logout

from braces.views import (
    LoginRequiredMixin, SuperuserRequiredMixin, GroupRequiredMixin)
from ipware.ip import get_ip
from .models import *

from .models import AuditTrial, AUDIT_TYPE_CHOICES

AUDIT_CHOICES = dict(AUDIT_TYPE_CHOICES)


class AuthMixin(SuperuserRequiredMixin):
    login_url = reverse_lazy('geeks_app:admin_login')


class EmployeeRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('geeks_app:user_login')


def storeAuditTrial(prevObj, changeObj, actionType, request):

    aTrial = AuditTrial()
    aTrial.modelType = changeObj._meta.verbose_name.title()
    aTrial.objectId = changeObj.pk
    aTrial.action = actionType
    aTrial.user = request.user
    aTrial.ip = get_ip(request)

    if prevObj:
        aTrial.fromObj = serializers.serialize("json", [prevObj])
    aTrial.toObj = serializers.serialize("json", [changeObj])
    aTrial.save()


class ListMixin(ListView):

    def get_queryset(self):
        if self.model is not None:
            queryset = self.model.objects.filter(
                deleted_at__isnull=True).order_by('-created_at')
            return queryset
        else:
            super().get_queryset()


class CreateMixin(CreateView):

    def form_valid(self, form):
        creator = User.objects.get(username=self.request.user)
        form.instance.created_by = creator
        obj = form.save()

        for k, v in AUDIT_CHOICES.items():
            if v == "CREATE":
                key = k
                storeAuditTrial('', obj, key, self.request)

        return super().form_valid(form)


class UpdateMixin(UpdateView):

    def form_valid(self, form):
        creator = User.objects.get(username=self.request.user)
        form.instance.created_by = creator
        prev_obj = self.get_object()
        obj = form.save()

        for k, v in AUDIT_CHOICES.items():
            if v == "UPDATE":
                key = k
                storeAuditTrial(prev_obj, obj, key, self.request)
        return super().form_valid(form)


class DeleteMixin(UpdateView):
    fields = ['deleted_at']

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        obj = form.save()
        for k, v in AUDIT_CHOICES.items():
            if v == 'DELETE':
                key = k
                storeAuditTrial('', obj, key, self.request)
        return super().form_valid(form)


class FrontendMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #########for advertisement part #######################
        context['add_below_menubar_full'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=3)[:2]
        context['add_below_menubar_half'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=4)[:4]
        context['ad_below_headling_full'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=9)[:2]
        context['ad_below_headling_half'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=10)[:2]
        context['ad_below_category_half'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=11)[:4]
        context['ad_above_footer_full'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=12)[:2]
        context['ad_above_footer_half'] = Advertisement.objects.filter(
            deleted_at__isnull=True, ad_type=13)[:3]

        context['recentpost'] = Post.objects.filter(
            publish=True, deleted_at__isnull=True).order_by('-created_at')[1:5]
        try:
            print(self.kwargs['slug'])
            context['category'] = Category.objects.get(
                slug=self.kwargs['slug'])
            context['post'] = context['category'].Category.all()
            print(context['post'])
        except:
            context['post'] = []
        # for dynamic menus in navbar ##################3
        main_menu = Menu.objects.filter(
            deleted_at__isnull=True, parent=None).order_by(
            '-updated_at').order_by('position')

        context['main_menu'] = main_menu
        return context
