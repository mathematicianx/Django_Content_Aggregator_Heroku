from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import News, Movie, MovieSpectacles, SimpleAd, Profile, ForumTopic, ForumResponse, User
from .forms import SimpleAdForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, CreateTopicForm, CreateResponseForm
from .custom_webscraper import olawa24_scraper, tuolawa_scraper, kino_odra_scraper, go_kino_scraper, um_olawa_scraper
from django.utils import timezone
from django.shortcuts import redirect
from django.views import View

class indexClassView(View):
    def get(self, request):
        return HttpResponse('it works')

def index(request):
    kino_odra_movies = Movie.objects.filter(which_site='kino_odra').filter(day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
    kino_odra_spectacles = {}
    for one_movie in kino_odra_movies:
        dates2 = []
        for c in one_movie.all_spectacles.all():
            dates2.append(c.date.strftime('%H:%M'))
        kino_odra_spectacles[one_movie] = dates2


    gokino_movies = Movie.objects.filter(which_site='gokino').filter(day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
    gokino_spectacles = {}
    for one_movie in gokino_movies:
        dates1 = []
        for d in one_movie.all_spectacles.all():
            dates1.append(d.date.strftime('%H:%M'))
        gokino_spectacles[one_movie] = dates1


    olawa24_news = News.objects.filter(which_site='olawa24').order_by('-date_of_publication')[:10]
    tuolawa_news = News.objects.filter(which_site='tuolawa').order_by('-date_of_publication')[:10]
    umolawa_news = News.objects.filter(which_site='umolawa').order_by('-date_of_publication')[:5]


    return render(request, 'homepage/index.html', {'olawa24_news': olawa24_news,
                                                        'tuolawa_news': tuolawa_news,
                                                        'kino_odra_movies': kino_odra_spectacles,
                                                        'gokino_movies': gokino_spectacles,
                                                        'umolawa_news': umolawa_news,
                                                        })

def show_all_ads(request):
    all_ads = SimpleAd.objects.all().order_by('-id')
    return render(request, 'homepage/show_all_ads.html', {'all_ads': all_ads})



def ad_detail(request, year, month, day, ad):
    ad = get_object_or_404(SimpleAd,
                           slug=ad,
                           date_of_publication__year=year,
                           date_of_publication__month=month,
                           date_of_publication__day=day)

    return render(request, 'homepage/ad_detail.html', {'ad': ad})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Uwierzytelnienie zakończyło się sukcesem')
                    # return HttpResponse('Uwierzytelnienie zakończyło się sukcesem')
                else:
                    messages.success(request, 'Konto jest zablokowane')
                    # return HttpResponse('Konto jest zablokowane')
            else:
                messages.success(request, 'Nieprawidłowe dane uwierzytelniające')
                # return HttpResponse('Nieprawidłowe dane uwierzytelniające')
    else:
        form = LoginForm()
    return render(request, 'homepage/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            messages.success(request, 'Uwierzytelnienie zakończyło się sukcesem')
            return render(request,
                          'homepage/register_done.html',
                          {'new_user': new_user}
                          )
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'homepage/register.html',
                      {'user_form': user_form}
                      )


def new_ad(request):
    all_ads = SimpleAd.objects.all()
    if request.method == 'POST':
        ad_form = SimpleAdForm(user=request.user, data=request.POST,
                               files=request.FILES)
        if ad_form.is_valid():
            new_ad = ad_form.save(commit=False)
            new_ad.author = request.user
            new_ad.save()
            ad_form = SimpleAdForm(user=request.user)
            return redirect('homepage:show_all_ads')
    else:
        ad_form = SimpleAdForm(user=request.user)
    return render(request, 'homepage/new_ad.html', {'ad_form': ad_form,
                                                    'all_ads': all_ads})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'homepage/edit.html', {'user_form': user_form,
                                                  'profile_form': profile_form})


def forum(request):
    all_topics = ForumTopic.objects.all().order_by('-id')
    return render(request, 'homepage/forum.html', {'all_topics': all_topics})


@login_required
def create_topic(request):
    if request.method == 'POST':
        new_topic_form = CreateTopicForm(user=request.user, data=request.POST)
        if new_topic_form.is_valid():
            new_topic = new_topic_form.save(commit=False)
            new_topic.author = request.user
            new_topic.save()
            new_topic_form = CreateTopicForm(user=request.user)
            return redirect('homepage:forum')
    else:
        new_topic_form = CreateTopicForm(user=request.user)

    return render(request,
                  'homepage/create_topic.html', {'new_topic_form': new_topic_form})


def post_detail(request, id, slug):
    post_topic = get_object_or_404(ForumTopic,
                                   slug=slug,
                                   id=id)

    try:
        post_responses = ForumResponse.objects.select_related('author__profile').filter(topic=post_topic).order_by('date_of_publication')
    except Exception:
        post_responses = ''

    topic_author_thumbnail_url = post_topic.author.profile.thumbnail.url

    if request.method == 'POST':
        new_response_form = CreateResponseForm(user=request.user, data=request.POST)
        if new_response_form.is_valid():
            new_response = new_response_form.save(commit=False)
            new_response.author = request.user
            new_response.topic = post_topic
            new_response.save()
            new_response_form = CreateResponseForm(user=request.user)

    else:
        new_response_form = CreateResponseForm(user=request.user)

    return render(request, 'homepage/post_detail.html', {'post_topic': post_topic,
                                                         'post_responses': post_responses,
                                                         'thumbnail_url': topic_author_thumbnail_url,
                                                         'new_response_form': new_response_form})


def local_news(request):
    olawa24_news = News.objects.filter(which_site='olawa24').order_by('-date_of_publication')
    tuolawa_news = News.objects.filter(which_site='tuolawa').order_by('-date_of_publication')

    return render(request, 'homepage/local_news.html', {'olawa24_news': olawa24_news,
                                                        'tuolawa_news': tuolawa_news})


def all_cityhall_news(request):
    umolawa_news = News.objects.filter(which_site='umolawa').order_by('-date_of_publication')
    return render(request, 'homepage/all_cityhall_news.html', {'umolawa_news': umolawa_news})
