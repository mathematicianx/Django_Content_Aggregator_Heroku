from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import News, Movie, MovieSpectacles, SimpleAd, Profile, ForumTopic, ForumResponse, User
from .forms import SimpleAdForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, CreateTopicForm, CreateResponseForm
from .custom_webscraper import olawa24_scraper, tuolawa_scraper, kino_odra_scraper, go_kino_scraper, um_olawa_scraper
from django.utils import timezone


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
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem')
                else:
                    return HttpResponse('Konto jest zablokowane')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające')
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
            return render(request,
                          'homepage/register_done.html',
                          {'new_user': new_user}
                          )
    else:
        user_form =UserRegistrationForm()
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


def create_topic(request):
    if request.method == 'POST':
        new_topic_form = CreateTopicForm(data=request.POST)
        if new_topic_form.is_valid():
            new_topic = new_topic_form.save()
            new_topic_form = CreateTopicForm()
    else:
        new_topic_form = CreateTopicForm()

    return render(request,
                  'homepage/create_topic.html', {'new_topic_form': new_topic_form})


def post_detail(request, id, slug):
    post_topic = get_object_or_404(ForumTopic,
                                   slug=slug,
                                   id=id)

    try:
        post_responses = ForumResponse.objects.select_related('author__profile').filter(topic=post_topic)
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


def save_data_from_scrapers():
    returned_dict = olawa24_scraper()
    for key in returned_dict:
        try:
            news = News.objects.get(title=key)
        except Exception:
            news = News()
            news.title = key
            news.link = returned_dict[key]['link']
            news.date_of_publication = returned_dict[key]['date']
            news.which_site = news.STATUS_olawa24
            news.save()


    returned_dict2 = tuolawa_scraper()
    for key in returned_dict2:
        try:
            news2 = News.objects.get(title=key)
        except Exception:
            news2 = News()
            news2.title = key
            news2.link = returned_dict2[key]['link']
            news2.date_of_publication = returned_dict2[key]['date']
            news2.which_site = news2.STATUS_tuolawa
            news2.save()


    returned_dict3 = kino_odra_scraper()
    for key in returned_dict3:
        compare_date = returned_dict3[key]['time_of_spectacles'][0].replace(hour=0, minute=0, second=0, microsecond=0)
        try:
            movie1 = Movie.objects.get(title=key, which_site='kino_odra', day_of_spectacle=compare_date)
        except:
            movie1 = Movie()
            movie1.title = key
            movie1.link = returned_dict3[key]['link']
            movie1.which_site = movie1.STATUS_kinoodra
            movie1.duration = returned_dict3[key]['duration']
            movie1.day_of_spectacle = returned_dict3[key]['time_of_spectacles'][0].replace(hour=0, minute=0, second=0, microsecond=0)
            movie1.filmweb_score = returned_dict3[key]['filmweb_score']
            movie1.save()
            many_times = returned_dict3[key]['time_of_spectacles']
            for single_time in many_times:
                try:
                    MovieSpectacles.objects.get(date=single_time, movie_name=Movie.objects.get(title=key, which_site='kino_odra', day_of_spectacle=compare_date))
                except:
                    single_time_of_spectacle = MovieSpectacles()
                    single_time_of_spectacle.movie_name = Movie.objects.get(title=key, which_site='kino_odra', day_of_spectacle=compare_date)
                    single_time_of_spectacle.date = single_time
                    single_time_of_spectacle.save()


    kino_odra_movies = Movie.objects.filter(which_site='kino_odra').filter(day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
    kino_odra_spectacles = {}
    for one_movie in kino_odra_movies:
        dates2 = []
        for c in one_movie.all_spectacles.all():
            dates2.append(c.date.strftime('%H:%M'))
        kino_odra_spectacles[one_movie] = dates2


    returned_dict4 = go_kino_scraper()
    for key in returned_dict4:
        compare_date = returned_dict4[key]['time_of_spectacles'][0].replace(hour=0, minute=0, second=0, microsecond=0)
        try:
            movie2 = Movie.objects.get(title=key, which_site='gokino', day_of_spectacle=compare_date)
        except Exception:
            movie2 = Movie()
            movie2.title = key
            movie2.link = returned_dict4[key]['link']
            movie2.which_site = movie2.STATUS_gokino
            movie2.duration = returned_dict4[key]['duration']
            movie2.day_of_spectacle = returned_dict4[key]['time_of_spectacles'][0].replace(hour=0, minute=0, second=0, microsecond=0)
            movie2.filmweb_score = returned_dict4[key]['filmweb_score']
            movie2.save()
            many_times = returned_dict4[key]['time_of_spectacles']
            for single_time in many_times:
                try:
                    MovieSpectacles.objects.get(date=single_time, movie_name=Movie.objects.get(title=key, which_site='gokino', day_of_spectacle=compare_date))
                except:
                    single_time_of_spectacle = MovieSpectacles()
                    single_time_of_spectacle.movie_name = Movie.objects.get(title=key, which_site='gokino', day_of_spectacle=compare_date)
                    single_time_of_spectacle.date = single_time
                    single_time_of_spectacle.save()

    gokino_movies = Movie.objects.filter(which_site='gokino').filter(day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
    gokino_spectacles = {}
    for one_movie in gokino_movies:
        dates1 = []
        for d in one_movie.all_spectacles.all():
            dates1.append(d.date.strftime('%H:%M'))
        gokino_spectacles[one_movie] = dates1


    returned_dict5 = um_olawa_scraper()
    for key in returned_dict5:
        try:
            news = News.objects.get(title=key, which_site='umolawa')
        except Exception:
            news = News()
            news.title = key
            news.link = returned_dict5[key]['link']
            news.date_of_publication = returned_dict5[key]['published_date']
            news.which_site = news.STATUS_umolawa
            news.content = returned_dict5[key]['content']
            news.save()
    olawa24_news = News.objects.filter(which_site='olawa24').order_by('-date_of_publication')[:10]
    tuolawa_news = News.objects.filter(which_site='tuolawa').order_by('-date_of_publication')[:10]
    umolawa_news = News.objects.filter(which_site='umolawa').order_by('-date_of_publication')[:5]