from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.forms import formset_factory
from django.http import Http404, JsonResponse
import urllib
from django.forms.utils import ErrorList
import requests

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Hall, Video
from .forms import VideoForm, SearchForm
# Create your views here.

YOUTUBE_API_KEY = 'AIzaSyCi1ODfgz82RsuTjF8jug4rVw3EfOjNTHY'

def home(request):
    return render(request, 'halls/home.html')

@login_required
def dashboard(request):
    halls = Hall.objects.filter(user=request.user)

    return render(request, 'halls/dashboard.html', {"halls": halls})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    # Login after sign up success
    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view

# CRUD Functions
class CreateHall(LoginRequiredMixin, generic.CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('home')

class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'


class UpdateHall(LoginRequiredMixin, generic.UpdateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/update_hall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(UpdateHall, self).get.object()
        if not hall.user == self.request.user:
            raise Http404

class DeleteHall(LoginRequiredMixin, generic.DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(DeleteHall, self).get.object()
        if not hall.user == self.request.user:
            raise Http404

@login_required
def add_video(request, pk):

    form = VideoForm()

    search_form = SearchForm()
    # Validate that the owner is adding videos
    hall = Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404
    if request.method == 'POST':
        # Create Form
        form = VideoForm(request.POST)

        # Validate the form
        if form.is_valid():
            # Create Video model object
            video = Video()
            video.hall = hall
            # Assign form inputs to model object
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')

            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')

                json = response.json()
                video.title = json['items'][0]['snippet']['title']

                video.save()
                return redirect('detail_hall', pk)

            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append("Needs to be a YouTube URL!!!")

    return render(request, 'halls/add_video.html', {'form':form, 'search_form':search_form, "hall":hall})

@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    print(search_form)
    if search_form.is_valid():
        #
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={encoded_search_term}&key={YOUTUBE_API_KEY}')
        return JsonResponse(response.json())
    else:
        print("Form is wrong")
        return JsonResponse({'message':'This is broken'})

class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'halls/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get.object()
        if not video.hall.user == self.request.user:
            raise Http404
