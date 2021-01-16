from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from homepage.models import SimpleAd, ForumTopic, News, Movie, MovieSpectacles, Profile
from homepage.views import IndexClassView, ShowAds, Register, NewAd, Edit, ForumView, CreateTopic, PostDetail,\
                           LocalNews, CityhallNews, AdDetail, Gallery
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


    def test_ad_detail_url_resolves_AdDetail_as_view(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        ad = SimpleAd.objects.create(title='test ad', slug='test-ad', body='test body',
                                     date_of_publication=timezone.now().replace(second=0, microsecond=0),
                                     price=250, author=self.user)

        year = ad.date_of_publication.year
        month = ad.date_of_publication.strftime('%m')
        day = ad.date_of_publication.strftime('%d')
        found = resolve(f'/{year}/{month}/{day}/{ad.slug}/'.format(year, month, day, ad.slug))
        self.assertEqual(found.func.__name__, AdDetail.as_view().__name__)

    def test_post_detail_url_resolves_PostDetail_as_view(self):
        found = resolve('/1/test/')
        self.assertEqual(found.func.__name__, PostDetail.as_view().__name__)
        self.assertEqual(found.func.__module__, PostDetail.as_view().__module__)

        # TODO I don't know how to test this with token, see below
        """
         path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        """
    def test_gallery_url_resolves_Gallery_as_view(self):
        found = resolve('/gallery/')
        self.assertEqual(found.func.__name__, Gallery.as_view().__name__)
        self.assertEqual(found.func.__module__, PostDetail.as_view().__module__)




class ViewRendersCorrectHTMLTemplate(TestCase):
    def test_IndexClassView_returns_correct_template(self):
        response = self.client.get('')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Oława</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_ShowAds_returns_correct_template(self):
        response = self.client.get('/show_all_ads/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Aktualne ogłoszenia</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_AdDetail_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        ad = SimpleAd.objects.create(title='test ad', slug='test-ad', body='test body',
                                     date_of_publication=timezone.now().replace(second=0, microsecond=0),
                                     price=250, author=self.user)
        year = ad.date_of_publication.year
        month = ad.date_of_publication.strftime('%m')
        day = ad.date_of_publication.strftime('%d')
        response = self.client.get(f'/{year}/{month}/{day}/{ad.slug}/'.format(year, month, day, ad.slug))
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>' + ad.title + '</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_Login_returns_correct_template(self):
        response = self.client.get('/login/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Logowanie</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_Register_returns_correct_template(self):
        response = self.client.get('/register/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Utwórz konto</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_NewAd_returns_correct_template(self):
        response = self.client.get('/new_ad/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Dodaj ogłoszenie</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_Edit_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.get('/edit/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Edycja konta</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_Forum_returns_correct_template(self):
        response = self.client.get('/forum/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Forum dyskusyjne</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_CreateTopic_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.get('/create_topic/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Stwórz nowy temat</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_PostDetail_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        topic = ForumTopic.objects.create(author=self.user, title='test title', body='test body',
                                          date_of_publication=timezone.now(), slug='test-title')
        response = self.client.get('/' + str(topic.id) + '/' + topic.slug + '/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>' + topic.title +'</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_AllCityhallNews_returns_correct_template(self):
        response = self.client.get('/all_cityhall_news/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Ogłoszenia z Urzędu Miasta</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_LocalNews_returns_correct_template(self):
        response = self.client.get('/local_news/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertIn('<title>Lokalne wiadomości</title>', html)
        self.assertTrue(html.endswith('</html>'))


class ModelCreatesCorrectly(TestCase):
    def create_news(self, title='Test news', link='http://www.test_link.com', content='content of a news',
                    which_site='olawa24', date_of_publication=timezone.now()):
        return News.objects.create(title=title, link=link, content=content, which_site=which_site,
                                   date_of_publication=date_of_publication)

    def test_news_creation(self):
        n = self.create_news()
        self.assertTrue(isinstance(n, News))
        self.assertEqual(n.__str__(), n.title)

    def create_movie(self, title='Title of a movie', link='http://www.test_link_for_a_movie.com', which_site='gokino',
                     duration=60, day_of_spectacle=timezone.now().replace(second=0, microsecond=0), filmweb_score=7.6):
        return Movie.objects.create(title=title, link=link, which_site=which_site, duration=duration,
                                    day_of_spectacle=day_of_spectacle, filmweb_score=filmweb_score)

    def test_movie_creation(self):
        m = self.create_movie()
        self.assertTrue(isinstance(m, Movie))
        self.assertEqual(m.link, 'http://www.test_link_for_a_movie.com')
        self.assertEqual(m.title, 'Title of a movie')
        self.assertEqual(m.which_site, 'gokino')
        self.assertEqual(m.duration, 60)
        self.assertEqual(m.day_of_spectacle, timezone.now().replace(second=0, microsecond=0))
        self.assertEqual(m.filmweb_score, 7.6)
        self.assertEqual(m.__str__(), m.title)

    def create_MovieSpectacle(self):
        m = self.create_movie()
        m.save()
        return MovieSpectacles.objects.create(movie_name=Movie.objects.get(id=1),
                                              date=timezone.now().replace(second=0, microsecond=0))

    def test_MovieSpectacle_creation(self):
        spectacle = self.create_MovieSpectacle()
        self.assertTrue(isinstance(spectacle, MovieSpectacles))
        self.assertEqual(spectacle.__unicode__(), 'Title of a movie')
        self.assertEqual(spectacle.date, timezone.now().replace(second=0, microsecond=0))



    def create_SimpleAd_with_photo(self, title='test ad', slug='test-ad', body='test body',
                                   date_of_publication=timezone.now().replace(second=0, microsecond=0), price=250):
        file_path = os.path.join(BASE_DIR, 'homepage\static\images\default.png')
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        test_object = SimpleAd.objects.create(title=title, slug=slug, body=body,
                                              date_of_publication=date_of_publication, price=price, author=self.user)
        test_object.image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read())
        return test_object


    def test_SimpleAd_with_photo(self):
        ad = self.create_SimpleAd_with_photo()
        year = ad.date_of_publication.year
        month = ad.date_of_publication.strftime('%m')
        day = ad.date_of_publication.strftime('%d')

        self.assertTrue(isinstance(ad, SimpleAd))
        self.assertEqual(ad.__str__(), ad.title)
        self.assertEqual(ad.title, 'test ad')
        self.assertEqual(ad.slug, 'test-ad')
        self.assertEqual(ad.body, 'test body')
        self.assertEqual(ad.date_of_publication.replace(second=0, microsecond=0), timezone.now().replace(second=0,
                                                                                                         microsecond=0))
        self.assertEqual(ad.price, 250)
        self.assertEqual(ad.author.username, 'test_user1')
        self.assertTrue(isinstance(ad.author, User))
        self.assertEqual(ad.image.name, 'test_image.jpg')
        self.assertEqual(ad.get_absolute_url(), f'/{year}/{month}/{day}/{ad.slug}/'.format(year, month, day, ad.slug))

