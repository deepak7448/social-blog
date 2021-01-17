from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View,TemplateView,DeleteView,UpdateView,RedirectView,DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from .models import Profiles
from .forms import ProfilesForm,UserupdateForm

# Create your views here

class profileView(LoginRequiredMixin,View):
    def get(self, request,*args, **kwargs):
        profiles = Profiles.objects.get(user=request.user)
        context={'profiles':profiles,}      
        return render(request,'profile/profile.html',context)
        
class ProfilesDetail(LoginRequiredMixin,DetailView):
    model = Profiles
    template_name='profile/profile.html'

class Updateprofile(LoginRequiredMixin,View):
    def get(self,request,slug,*args, **kwargs):
        try:
            profiles = Profiles.objects.get(slug=slug)
        except Profiles.DoesNotExist:
            #return render(request, "home.html") 
            return render(request,'404.html')
            #raise Http404("No MyModel matches the given query.")
        p_form = ProfilesForm(instance=profiles)
        u_form = UserupdateForm(instance=request.user)
        context={'p_form':p_form,'u_form':u_form,'profiles':profiles}   
        return render(request,'profile/update_profile.html',context)

    def post(self,request,slug,*args,**kwargs):
        profiles = Profiles.objects.get(slug=slug)
        p_form = ProfilesForm(request.POST or None,request.FILES or None,instance=profiles)
        u_form = UserupdateForm(request.POST or None,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Your Profile has been updated.')
        return redirect("profile:profiles",username=profiles.user.username)

def error_404(request,exception):
    return render(request,'404.html')

def error_403(request,exception):
    return render(request,'403.html')

def error_400(request,exception):
    return render(request,'400.html')

def error_500(request,exception):
    return render(request,'500.html')