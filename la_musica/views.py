from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View, DetailView


from .forms import CreateFlatSheetMusicForm, CreateGroupForm
from .models import Group, FlatSheetMusic



class LoginView(View):
    template_name = "login.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("sheet_music_list")

        return render(request, self.template_name)
    


    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("sheet_music_list")
        
        else:
            return render(request, self.template_name, {"error": _("Invalid email or password")})

class CreateFlatSheetMusic(LoginRequiredMixin, CreateView):
    form_class = CreateFlatSheetMusicForm
    template_name = "create_glucose_record.html"
    success_url = reverse_lazy("sheet_music_list")
    message = _("Glucose measure added succesfully!")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(self.request, message=self.message)
        
        return response

class HomeView(DetailView):
    template_name = "home.html"
    model = FlatSheetMusic
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        
        sheet_music_names = FlatSheetMusic.objects.all()
        
        context_data["sheet_music_list"] = sheet_music_names
        
        return context_data
    

class UpdateFlatSheetMusic(CreateFlatSheetMusic, UpdateView):
    template_name = "update_glucose_record.html"
    model = FlatSheetMusic
    message = _("Glucose measure modified succesfully!")

class DeleteFlatSheetMusic(LoginRequiredMixin, DeleteView):
    template_name = "delete_glucose_record.html"
    model = FlatSheetMusic
    success_url = reverse_lazy("sheet_music_list")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, message=_("Glucose measure removed succesfully!"))
        
        return response

class ListFlatSheetMusic(LoginRequiredMixin, ListView):
    template_name = "list_sheet_music.html"
    
    def get_queryset(self):
        return FlatSheetMusic.objects.all().order_by("title")


class CreateGroup(LoginRequiredMixin, CreateView):
    form_class = CreateGroupForm
    template_name = "create_glucose_record.html"
    success_url = reverse_lazy("sheet_music_list")
    message = _("Glucose measure added succesfully!")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        messages.success(self.request, message=self.message)
        
        return response


class UpdateGroup(CreateGroup, UpdateView):
    template_name = "update_glucose_record.html"
    model = Group
    message = _("Glucose measure modified succesfully!")

class DeleteGroup(LoginRequiredMixin, DeleteView):
    template_name = "delete_glucose_record.html"
    model = Group
    success_url = reverse_lazy("sheet_music_list")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, message=_("Glucose measure removed succesfully!"))
        
        return response

class ListGroup(LoginRequiredMixin, ListView):
    template_name = "list_glucose_record.html"
    
    def get_queryset(self):
        return FlatSheetMusic.objects.filter(user__pk=self.request.user.pk).order_by("date")
