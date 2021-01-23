from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import News, Movie, MovieSpectacles, SimpleAd, Profile, ForumTopic, ForumResponse, User, Gallery
from .forms import SimpleAdForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, CreateTopicForm, CreateResponseForm, AddImageToGalleryForm
from .custom_webscraper import olawa24_scraper, tuolawa_scraper, kino_odra_scraper, go_kino_scraper, um_olawa_scraper
from django.utils import timezone
from django.shortcuts import redirect
from django.views import View


class IndexClassView(View):
    def get(self, request):

        olawa24_news = News.olawa24_manager.all().order_by('-date_of_publication')[:10]
        tuolawa_news = News.tuolawa_manager.all().order_by('-date_of_publication')[:10]
        umolawa_news = News.umolawa_manager.all().order_by('-date_of_publication')[:5]
        kino_odra_movies = Movie.kino_odra_manager.all().filter(day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
        kino_odra_spectacles = {}
        for one_movie in kino_odra_movies:
            spectacle_dates_list = []
            for spectacle_date in one_movie.all_spectacles.all():
                spectacle_dates_list.append(spectacle_date.date.strftime('%H:%M'))
            kino_odra_spectacles[one_movie] = spectacle_dates_list

        go_kino_movies = Movie.gokino_manager.all().filter(day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
        go_kino_spectacles = {}
        for one_movie2 in go_kino_movies:
            spectacle_dates_list2 = []
            for spectacle_date2 in one_movie2.all_spectacles.all():
                spectacle_dates_list2.append(spectacle_date2.date.strftime('%H:%M'))
            go_kino_spectacles[one_movie2] = spectacle_dates_list2

        return render(request, 'homepage/index.html', {'olawa24_news': olawa24_news,
                                                       'tuolawa_news': tuolawa_news,
                                                       'umolawa_news': umolawa_news,
                                                       'kino_odra_movies': kino_odra_spectacles,
                                                       'go_kino_spectacles': go_kino_spectacles})


class ShowAds(View):
    def get(self, request):
        all_ads = SimpleAd.objects.all().order_by('-id')
        return render(request, 'homepage/show_all_ads.html', {'all_ads': all_ads})


class AdDetail(View):
    def get(self, request, year, month, day, ad):
        ad = get_object_or_404(SimpleAd,
                               slug=ad,
                               date_of_publication__year=year,
                               date_of_publication__month=month,
                               date_of_publication__day=day)
        return render(request, 'homepage/ad_detail.html', {'ad': ad})

# basic login function,it was replaced by integrated in django loginview, I am leaving it here just to know how to do it
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     messages.success(request, 'Uwierzytelnienie zakończyło się sukcesem')
#                     # return HttpResponse('Uwierzytelnienie zakończyło się sukcesem')
#                 else:
#                     messages.success(request, 'Konto jest zablokowane')
#                     # return HttpResponse('Konto jest zablokowane')
#             else:
#                 messages.success(request, 'Nieprawidłowe dane uwierzytelniające')
#                 # return HttpResponse('Nieprawidłowe dane uwierzytelniające')
#     else:
#         form = LoginForm()
#     return render(request, 'homepage/login.html', {'form': form})


class Register(View):
    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'homepage/register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            messages.success(request, 'Uwierzytelnienie zakończyło się sukcesem')
            return render(request, 'homepage/register_done.html', {'new_user': new_user})


class NewAd(View):
    all_ads = SimpleAd.objects.all()
    def post(self, request):
        ad_form = SimpleAdForm(user=request.user,data=request.POST, files=request.FILES)
        if ad_form.is_valid():
            new_ad = ad_form.save(commit=False)
            new_ad.author = request.user
            new_ad.save()
            ad_form = SimpleAdForm(user=request.user)
            return redirect('homepage:show_all_ads')

    def get(self, request):
        ad_form = SimpleAdForm(user=request.user)
        return render(request, 'homepage/new_ad.html', {'ad_form': ad_form,
                                                        'all_ads': self.all_ads})

class Edit(View):

    @method_decorator(login_required)
    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('homepage:index')

    @method_decorator(login_required)
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'homepage/edit.html', {'user_form': user_form,
                                                      'profile_form': profile_form})


class ForumView(View):
    def get(self, request):
        all_topics = ForumTopic.objects.all().order_by('-id')
        return render(request, 'homepage/forum.html', {'all_topics': all_topics})


class CreateTopic(View):
    @method_decorator(login_required)
    def post(self, request):
        new_topic_form = CreateTopicForm(user=request.user, data=request.POST)
        if new_topic_form.is_valid():
            new_topic = new_topic_form.save(commit=False)
            new_topic.author = request.user
            new_topic.save()
            new_topic_form = CreateTopicForm(user=request.user)
            return redirect('homepage:forum')

    @method_decorator(login_required)
    def get(self, request):
        new_topic_form = CreateTopicForm(user=request.user)
        return render(request, 'homepage/create_topic.html', {'new_topic_form': new_topic_form})


class PostDetail(View):
    def get(self, request, slug, id):
        post_topic = get_object_or_404(ForumTopic,
                                       slug=slug,
                                       id=id)

        try:
            post_responses = ForumResponse.objects.select_related('author__profile').filter(topic=post_topic).order_by('date_of_publication')
        except AttributeError:
            post_responses = ''
        try:
            topic_author_thumbnail_url = post_topic.author.profile.thumbnail.url
        except AttributeError:
            topic_author_thumbnail_url = None

        new_response_form = CreateResponseForm(user=request.user)
        return render(request, 'homepage/post_detail.html', {'post_topic': post_topic,
                                                             'post_responses': post_responses,
                                                             'thumbnail_url': topic_author_thumbnail_url,
                                                             'new_response_form': new_response_form})

    @method_decorator(login_required)
    def post(self, request, id, slug):
        post_topic = get_object_or_404(ForumTopic,
                                       slug=slug,
                                       id=id)
        try:
            post_responses = ForumResponse.objects.select_related('author__profile').filter(topic=post_topic).order_by('date_of_publication')
        except AttributeError:
            post_responses = ''
        try:
            topic_author_thumbnail_url = post_topic.author.profile.thumbnail.url
        except AttributeError:
            topic_author_thumbnail_url = None

        new_response_form = CreateResponseForm(user=request.user, data=request.POST)
        if new_response_form.is_valid():
            new_response = new_response_form.save(commit=False)
            new_response.author = request.user
            new_response.topic = post_topic
            new_response.save()
            new_response_form = CreateResponseForm(user=request.user)
        return render(request, 'homepage/post_detail.html', {'post_topic': post_topic,
                                                             'post_responses': post_responses,
                                                             'thumbnail_url': topic_author_thumbnail_url,
                                                             'new_response_form': new_response_form})


class LocalNews(View):
    def get(self, request):
        olawa24_news = News.olawa24_manager.order_by('-date_of_publication')
        tuolawa_news = News.tuolawa_manager.order_by('-date_of_publication')

        return render(request, 'homepage/local_news.html', {'olawa24_news': olawa24_news,
                                                            'tuolawa_news': tuolawa_news})


class CityhallNews(View):
    def get(self, request):
        umolawa_news = News.umolawa_manager.order_by('-date_of_publication')
        return render(request, 'homepage/all_cityhall_news.html', {'umolawa_news': umolawa_news})

class GalleryView(View):
    def get(self, request):
        gallery_images = Gallery.objects.all()
        last_image = Gallery.objects.latest('id')

        short_table = []
        long_table = []

        for image in gallery_images:
            print(image)
            if len(short_table) < 4 and len(long_table) == 0:
                short_table.append(image)
                long_table.append(short_table)
            elif len(short_table) == 4 and len(long_table[-1]) == 4:
                long_table.append([image])
                short_table = [image]
            elif len(short_table) < 4 and len(long_table[-1]) < 4:
                short_table.append(image)
                long_table[-1] = short_table

<<<<<<< HEAD
=======


        print(last_image.image.url)
>>>>>>> f9b9be7646ad2c0ac3a25577477273c86055e737
        return render(request, 'homepage/gallery.html', {'gallery_images': gallery_images,
                                                         'long_table': long_table,
                                                         'last_image': last_image})

class AddImage(View):
    @method_decorator(login_required)
    def post(self, request):
        new_image_form = AddImageToGalleryForm(user=request.user, data=request.POST, files=request.FILES)
        if new_image_form.is_valid():
            new_image = new_image_form.save(commit=False)
            new_image.author = request.user
            new_image.save()
            new_image_form = AddImageToGalleryForm(user=request.user)
            return redirect('homepage:gallery')

    @method_decorator(login_required)
    def get(self, request):
        new_image_form = AddImageToGalleryForm(user=request.user)
        return render(request, 'homepage/add_image.html', {'new_image_form': new_image_form})
<<<<<<< HEAD
=======

class ChangeActiveImage(View):
    def post(self, request):
        id = request.POST.id
        print(id)
        image_id = request.POST.get('id')
        full_image = Gallery.objects.get(id=image_id)
        return render(request, 'homepage/gallery.html', {'full_image': full_image})
>>>>>>> f9b9be7646ad2c0ac3a25577477273c86055e737
