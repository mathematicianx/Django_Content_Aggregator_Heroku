from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'homepage'

urlpatterns = [
    path('', views.indexClassView.as_view(), name='index'),
    path('show_all_ads/', views.ShowAds.as_view(), name='show_all_ads'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('new_ad/', views.NewAd.as_view(), name='new_ad'),
    path('<int:year>/<int:month>/<int:day>/<slug:ad>/', views.AdDetail.as_view(), name='ad_detail'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('forum/', views.ForumView.as_view(), name='forum'),
    path('<int:id>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('local_news/', views.LocalNews.as_view(), name='local_news'),
    path('all_cityhall_news/', views.CityhallNews.as_view(), name='all_cityhall_news'),
    path('test/', views.NewAd.as_view(), name='test')
]

