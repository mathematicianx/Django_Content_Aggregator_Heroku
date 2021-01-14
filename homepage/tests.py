from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.utils import timezone
from homepage.models import SimpleAd, ForumTopic, News, Movie, MovieSpectacles
from homepage.views import IndexClassView, ShowAds, Register, NewAd, Edit, ForumView, CreateTopic, PostDetail, LocalNews, CityhallNews
import os
from mysite.settings import BASE_DIR


class UrlResolveCorrectViewTest(TestCase):

    def test_root_url_resolves_to_IndexClassView(self):
        found = resolve('/')
        self.assertEqual(found.func.__name__, IndexClassView.as_view().__name__)
        self.assertEqual(found.func.__module__, IndexClassView.as_view().__module__)

    def test_show_all_ads_url_resolves_to_ShowAds(self):
        found = resolve('/show_all_ads/')
        self.assertEqual(found.func.__name__, ShowAds.as_view().__name__)
        self.assertEqual(found.func.__module__, ShowAds.as_view().__module__)

    def test_register_url_resolves_Register(self):
        found = resolve('/register/')
        self.assertEqual(found.func.__name__, Register.as_view().__name__)
        self.assertEqual(found.func.__module__, Register.as_view().__module__)

    def test_new_ad_url_resolves_NewAd(self):
        found = resolve('/new_ad/')
        self.assertEqual(found.func.__name__, NewAd.as_view().__name__)
        self.assertEqual(found.func.__module__, NewAd.as_view().__module__)

    def test_edit_url_resolves_Edit(self):
        found = resolve('/edit/')
        self.assertEqual(found.func.__name__, Edit.as_view().__name__)
        self.assertEqual(found.func.__module__, Edit.as_view().__module__)

    def test_forum_url_resolves_forum(self):
        found = resolve('/forum/')
        self.assertEqual(found.func.__name__, ForumView.as_view().__name__)
        self.assertEqual(found.func.__module__, ForumView.as_view().__module__)

    def test_create_topic_url_resolves_CreateTopic(self):
        found = resolve('/create_topic/')
        self.assertEqual(found.func.__name__, CreateTopic.as_view().__name__)
        self.assertEqual(found.func.__module__, CreateTopic.as_view().__module__)

    def test_local_news_url_resolves_LocalNews(self):
        found = resolve('/local_news/')
        self.assertEqual(found.func.__name__, LocalNews.as_view().__name__)
        self.assertEqual(found.func.__module__, LocalNews.as_view().__module__)

    def test_all_cityhall_news_url_resolves_CityhallNews(self):
        found = resolve('/all_cityhall_news/')
        self.assertEqual(found.func.__name__, CityhallNews.as_view().__name__)
        self.assertEqual(found.func.__module__, CityhallNews.as_view().__module__)

    def test_login_url_resolves_auth_views_LoginView_as_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func.__name__, auth_views.LoginView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.LoginView.as_view().__module__)

    def test_logout_url_resolves_auth_views_LogoutView_as_view(self):
        found = resolve('/logout/')
        self.assertEqual(found.func.__name__, auth_views.LogoutView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.LogoutView.as_view().__module__)

    def test_password_change_url_resolves_auth_views_PasswordChangeView_as_view(self):
        found = resolve('/password_change/')
        self.assertEqual(found.func.__name__, auth_views.PasswordChangeView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.PasswordChangeView.as_view().__module__)

    def test_password_change_done_url_resolves_auth_views_PasswordChangeDoneView_as_view(self):
        found = resolve('/password_change/done/')
        self.assertEqual(found.func.__name__, auth_views.PasswordChangeDoneView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.PasswordChangeDoneView.as_view().__module__)

    def test_password_reset_url_resolves_auth_views_PasswordResetView_as_view(self):
        found = resolve('/password_reset/')
        self.assertEqual(found.func.__name__, auth_views.PasswordResetView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.PasswordResetView.as_view().__module__)

    def test_password_reset_done_url_resolves_auth_views_PasswordResetDoneView_as_view(self):
        found = resolve('/password_reset/done/')
        self.assertEqual(found.func.__name__, auth_views.PasswordResetDoneView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.PasswordResetDoneView.as_view().__module__)

    def test_password_reset_complete_url_resolves_auth_views_PasswordResetCompleteView_as_view(self):
        found = resolve('/reset/done/')
        self.assertEqual(found.func.__name__, auth_views.PasswordResetCompleteView.as_view().__name__)
        self.assertEqual(found.func.__module__, auth_views.PasswordResetCompleteView.as_view().__module__)

        """
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('<int:year>/<int:month>/<int:day>/<slug:ad>/', views.ad_detail, name='ad_detail'),
        path('<int:id>/<slug:slug>/', views.post_detail, name='post_detail'),
        """





# class ViewRendersCorrectHTMLTemplate(TestCase):
#     def test_index_view_returns_correct_html(self):
#         request = HttpRequest()
#         response = IndexClassView.as_view()
#         expected_html = render_to_string('homepage/index.html')
#         self.assertEqual(response.content.decode(), expected_html)
# #
#     def test_show_all_ads_view_returns_correct_html(self):
#         all_ads = SimpleAd.objects.all().order_by('-id')
#         request = HttpRequest()
#         response = show_all_ads(request)
#         expected_html = render_to_string('homepage/show_all_ads.html', {'all_ads': all_ads})
#         self.assertEqual(response.content.decode(), expected_html)
#
#     # def test_ad_detail_view_returns_correct_html(self):
#     #     request = HttpRequest()
#     #     response = show_all_ads(request)
#     #     expected_html = render_to_string('homepage/ad_detail.html')
#     #     self.assertEqual(response.content.decode(), expected_html)
#
#     def not_tested_user_login(self):
#         pass
#
#     def not_tested_register(self):
#         pass
#
#     def not_tested_new_ad(self):
#         pass
#
#     def not_tested_edit(self):
#         pass
#
#     def test_forum_view_returns_correct_html(self):
#         all_topics = ForumTopic.objects.all().order_by('-id')
#         request = HttpRequest()
#         response = forum(request)
#         expected_html = render_to_string('homepage/forum.html', {'all_topics': all_topics})
#         self.assertEqual(response.content.decode(), expected_html)
#
#     def not_tested_create_topic(self):
#         pass
#
#     def not_tested_post_detail(self):
#         pass
#
#     def test_local_news_returns_correct_html(self):
#         olawa24_news = News.objects.filter(which_site='olawa24').order_by('-id')
#         tuolawa_news = News.objects.filter(which_site='tuolawa').order_by('-id')
#         request = HttpRequest()
#         response = local_news(request)
#         expected_html = render_to_string('homepage/local_news.html', {'olawa24_news': olawa24_news,
#                                                                       'tuolawa_news': tuolawa_news})
#         self.assertEqual(response.content.decode(), expected_html)
#
#     def test_all_cityhall_news_returns_correct_html(self):
#         umolawa_news = News.objects.filter(which_site='umolawa').order_by('-date_of_publication')
#         request = HttpRequest()
#         response = all_cityhall_news(request)
#         expected_html = render_to_string('homepage/all_cityhall_news.html', {'umolawa_news': umolawa_news})
#         self.assertEqual(response.content.decode(), expected_html)
#
#
class ModelCreatesCorrectly(TestCase):
    def create_news(self, title='Test news', link='http://www.test_link.com', content='content of a news', which_site='olawa24', date_of_publication=timezone.now()):
        return News.objects.create(title=title, link=link, content=content, which_site=which_site, date_of_publication=date_of_publication)

    def test_news_creation(self):
        n = self.create_news()
        self.assertTrue(isinstance(n, News))
        self.assertEqual(n.__str__(), n.title)

    def create_movie(self, title='Title of a movie', link='http://www.test_link_for_a_movie.com', which_site='gokino', duration=60, day_of_spectacle=timezone.now(), filmweb_score=7.6):
        return Movie.objects.create(title=title, link=link, which_site=which_site, duration=duration, day_of_spectacle=day_of_spectacle, filmweb_score=filmweb_score)

    def test_movie_creation(self):
        m = self.create_movie()
        self.assertTrue(isinstance(m, Movie))
        self.assertEqual(m.__str__(), m.title)

    def create_MovieSpectacle(self):
        m = self.create_movie()
        m.save()
        return MovieSpectacles.objects.create(movie_name=Movie.objects.get(id=1), date=timezone.now())

    def test_MovieSpectacle_creation(self):
        spectacle = self.create_MovieSpectacle()
        self.assertTrue(isinstance(spectacle, MovieSpectacles))
        self.assertEqual(spectacle.__unicode__(), spectacle.movie_name)

    def create_SimpleAd_without_photo(self, title='test ad', slug='test_ad', body='test body', date_of_publication=timezone.now(), price=250):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        return SimpleAd.objects.create(title=title, slug=slug, body=body, date_of_publication=date_of_publication, price=price, author=self.user)

    def create_SimpleAd_with_photo(self, title='test ad', slug='test_ad', body='test body', date_of_publication=timezone.now(), price=250):
        file_path = os.path.join(BASE_DIR, 'homepage\static\images\default.png')
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        test_object = SimpleAd.objects.create(title=title, slug=slug, body=body, date_of_publication=date_of_publication, price=price,
                                author=self.user)
        test_object.image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read())
        return test_object


    def test_SimpleAd_without_photo(self):
        ad = self.create_SimpleAd_without_photo()
        self.assertTrue(isinstance(ad, SimpleAd))
        # self.assertEqual(ad.__str__(), ad.title)


    def test_SimpleAd_with_photo(self):
        ad = self.create_SimpleAd_with_photo()
        self.assertTrue(isinstance(ad, SimpleAd))
        # self.assertEqual(ad.__str__(), ad.title)






""" title = models.CharField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_ads')
    body = tinymce_models.HTMLField()
    date_of_publication = models.DateTimeField(auto_now_add=True)
    image = ThumbnailImageField(upload_to='uploads/',
                                blank=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_of_publication')
    price = models.IntegerField()

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnail(self.image, '200x200', quality=90)

    @property
    def resized_photo(self):
        if self.image:
            return get_thumbnail(self.image, '1000x1000', quality=90)


    def image_tag(self):
        return mark_safe('<img src="/media/%s"/>' % (self.thumbnail))

    image_tag.short_description = 'Thumbnail'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('homepage:ad_detail',
                       args=[self.date_of_publication.year,
                             self.date_of_publication.strftime('%m'),
                             self.date_of_publication.strftime('%d'),
                             self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        slug = self.slug
        while True:
            try:
                test_ad = SimpleAd.objects.get(slug=slug)
                if test_ad == self:
                    self.slug = slug
                    break
                else:
                    slug = slug + '1'
            except:
                self.slug = slug
                break
        super(SimpleAd, self).save(*args, **kwargs)
"""