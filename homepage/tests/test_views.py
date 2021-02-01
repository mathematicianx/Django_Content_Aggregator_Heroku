from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from django.utils.text import slugify
from homepage.models import SimpleAd, ForumTopic, News, Movie, MovieSpectacles, Profile, ForumResponse
from homepage.views import IndexClassView, ShowAds, Register, NewAd, Edit, ForumView, CreateTopic, PostDetail,\
                           LocalNews, CityhallNews, AdDetail, GalleryView



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
        ad = SimpleAd.objects.create(title='test ad', slug=slugify('test ad'), body='test body',
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
        self.assertEqual(found.func.__name__, GalleryView.as_view().__name__)
        self.assertEqual(found.func.__module__, PostDetail.as_view().__module__)


class ViewRendersCorrectHTMLTemplateForGetMethod(TestCase):
    def test_IndexClassView_returns_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'homepage/index.html')

    def test_ShowAds_returns_correct_template(self):
        response = self.client.get('/show_all_ads/')
        self.assertTemplateUsed(response, 'homepage/show_all_ads.html')

    def test_AdDetail_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        ad = SimpleAd.objects.create(title='test ad', slug=slugify('test ad'), body='test body',
                                     date_of_publication=timezone.now().replace(second=0, microsecond=0),
                                     price=250, author=self.user)
        year = ad.date_of_publication.year
        month = ad.date_of_publication.strftime('%m')
        day = ad.date_of_publication.strftime('%d')
        response = self.client.get(f'/{year}/{month}/{day}/{ad.slug}/'.format(year, month, day, ad.slug))
        self.assertTemplateUsed(response, 'homepage/ad_detail.html')


    def test_Login_returns_correct_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_Register_returns_correct_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'homepage/register.html')

    def test_NewAd_returns_correct_template(self):
        response = self.client.get('/new_ad/')
        self.assertTemplateUsed(response, 'homepage/new_ad.html')

    def test_Edit_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.get('/edit/')
        self.assertTemplateUsed(response, 'homepage/edit.html')

    def test_Forum_returns_correct_template(self):
        response = self.client.get('/forum/')
        self.assertTemplateUsed(response, 'homepage/forum.html')

    def test_CreateTopic_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.get('/create_topic/')
        self.assertTemplateUsed(response, 'homepage/create_topic.html')

    def test_PostDetail_returns_correct_template(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        topic = ForumTopic.objects.create(author=self.user, title='test title', body='test body',
                                          date_of_publication=timezone.now(), slug=slugify('test title'))
        response = self.client.get('/' + str(topic.id) + '/' + topic.slug + '/')
        self.assertTemplateUsed(response, 'homepage/post_detail.html')


    def test_AllCityhallNews_returns_correct_template(self):
        response = self.client.get('/all_cityhall_news/')
        self.assertTemplateUsed(response, 'homepage/all_cityhall_news.html')


    def test_LocalNews_returns_correct_template(self):
        response = self.client.get('/local_news/')
        self.assertTemplateUsed(response, 'homepage/local_news.html')

    def test_Gallery_returns_correct_template(self):
        response = self.client.get('/gallery/')
        self.assertTemplateUsed(response, 'homepage/gallery.html')

class ViewRendersCorrectTemplateForPostMethod(TestCase):
    def test_Register_post_method(self):
        response = self.client.post('/register/', data={'username': 'test_user2', 'first_name': 'imie testera',
                                                        'email': 'tester@testowytester.com', 'password': 'test_user2',
                                                        'password2': 'test_user2'})
        self.assertTemplateUsed(response, 'homepage/register_done.html')

    def test_NewAd_post_method(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.post('/new_ad/', data={'title': 'test ogloszenia',
                                                      'body': 'tresc ogloszenia',
                                                      'date_of_publication': timezone.now().replace(second=0,
                                                                                                    microsecond=0),
                                                      'slug': slugify('test ogloszenia'), 'price': 250},
                                    follow=True)
        self.assertTemplateUsed(response, 'homepage/show_all_ads.html')

    def test_CreateTopic_post_method(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.post('/create_topic/',
                                    data={'title': 'nazwa tematu',
                                    'body': 'tresc tematu',
                                    'date_of_publication': timezone.now().replace(second=0, microsecond=0),
                                    'slug': slugify('nazwa tematu')},
                                    follow=True)

        self.assertTemplateUsed(response, 'homepage/forum.html')

    def test_PostDetail_post_method(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        self.client.login(username='test_user1', password='test_user1')
        topic = ForumTopic.objects.create(author=self.user,
                                          title='tytul tematu',
                                          body='tresc tematu',
                                          date_of_publication=timezone.now().replace(hour=0,
                                                                                     minute=0,
                                                                                     second=0,
                                                                                     microsecond=0),
                                          slug=slugify('tytul tematu'))

        response = self.client.post(f'/{topic.id}/{topic.slug}/'.format(topic.id, topic.slug),
                                    data={'body': 'tresc posta',
                                    'date_of_publication': timezone.now().replace(second=0, microsecond=0),
                                    'topic': topic})
        self.assertTemplateUsed(response, 'homepage/post_detail.html')

    def test_Edit_post_method(self):
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        profile = Profile.objects.create(user=self.user,
                                         date_of_birth=timezone.now().replace(hour=0,
                                                                              minute=0,
                                                                              second=0,
                                                                              microsecond=0))
        self.client.login(username='test_user1', password='test_user1')
        response = self.client.post('/edit/', data={'date_of_birth': timezone.now()}, follow=True)
        self.assertTemplateUsed(response, 'homepage/index.html')

