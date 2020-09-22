from django.urls import resolve
from django.test import TestCase
from .models import SimpleAd, ForumTopic, News
from .views import index, show_all_ads, register, new_ad, edit, forum, create_topic, local_news, all_cityhall_news
from django.contrib.auth import views as auth_views
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

class UrlResolveCorrectViewTest(TestCase):

    def test_root_url_resolves_to_index(self):
        found = resolve('/')
        self.assertEqual(found.func, index),

    def test_show_all_ads_url_resolves_to_show_all_ads(self):
        found = resolve('/show_all_ads/')
        self.assertEqual(found.func, show_all_ads)

    def test_register_url_resolves_register(self):
        found = resolve('/register/')
        self.assertEqual(found.func, register)

    def test_new_ad_url_resolves_new_ad(self):
        found = resolve('/new_ad/')
        self.assertEqual(found.func, new_ad)

    def test_edit_url_resolves_edit(self):
        found = resolve('/edit/')
        self.assertEqual(found.func, edit)

    def test_forum_url_resolves_forum(self):
        found = resolve('/forum/')
        self.assertEqual(found.func, forum)

    def test_create_topic_url_resolves_create_topic(self):
        found = resolve('/create_topic/')
        self.assertEqual(found.func, create_topic)

    def test_local_news_url_resolves_local_news(self):
        found = resolve('/local_news/')
        self.assertEqual(found.func, local_news)

    def test_all_cityhall_news_url_resolves_all_cityhall_news(self):
        found = resolve('/all_cityhall_news/')
        self.assertEqual(found.func, all_cityhall_news)

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

class ViewRendersCorrectHTMLTemplate(TestCase):
    def test_index_view_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('homepage/index.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_show_all_ads_view_returns_correct_html(self):
        all_ads = SimpleAd.objects.all().order_by('-id')
        request = HttpRequest()
        response = show_all_ads(request)
        expected_html = render_to_string('homepage/show_all_ads.html', {'all_ads': all_ads})
        self.assertEqual(response.content.decode(), expected_html)

    # def test_ad_detail_view_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = show_all_ads(request)
    #     expected_html = render_to_string('homepage/ad_detail.html')
    #     self.assertEqual(response.content.decode(), expected_html)

    def not_tested_user_login(self):
        pass

    def not_tested_register(self):
        pass

    def not_tested_new_ad(self):
        pass

    def not_tested_edit(self):
        pass

    def test_forum_view_returns_correct_html(self):
        all_topics = ForumTopic.objects.all().order_by('-id')
        request = HttpRequest()
        response = forum(request)
        expected_html = render_to_string('homepage/forum.html', {'all_topics': all_topics})
        self.assertEqual(response.content.decode(), expected_html)

    def not_tested_create_topic(self):
        pass

    def not_tested_post_detail(self):
        pass

    def test_local_news_returns_correct_html(self):
        olawa24_news = News.objects.filter(which_site='olawa24').order_by('-id')
        tuolawa_news = News.objects.filter(which_site='tuolawa').order_by('-id')
        request = HttpRequest()
        response = local_news(request)
        expected_html = render_to_string('homepage/local_news.html', {'olawa24_news': olawa24_news,
                                                                      'tuolawa_news': tuolawa_news})
        self.assertEqual(response.content.decode(), expected_html)

    def test_all_cityhall_news_returns_correct_html(self):
        umolawa_news = News.objects.filter(which_site='umolawa').order_by('-date_of_publication')
        request = HttpRequest()
        response = all_cityhall_news(request)
        expected_html = render_to_string('homepage/all_cityhall_news.html', {'umolawa_news': umolawa_news})
        self.assertEqual(response.content.decode(), expected_html)

