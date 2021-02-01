from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from homepage.models import SimpleAd, ForumTopic, News, Movie, MovieSpectacles, Profile, ForumResponse
from homepage.custom_webscraper import olawa24_scraper, tuolawa_scraper, kino_odra_scraper, go_kino_scraper, um_olawa_scraper
import os
from mysite.settings import BASE_DIR


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


    def create_SimpleAd_with_photo(self, title='test ad', slug='test_ad', body='test body', date_of_publication=timezone.now(), price=250):
        file_path = os.path.join(BASE_DIR, 'homepage\static\images\default.png')
        self.user = User.objects.create_user(username='test_user1', password='test_user1')
        test_object = SimpleAd.objects.create(title=title, slug=slug, body=body, date_of_publication=date_of_publication, price=price,
                                author=self.user)
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

    def test_Profile_creation(self):
        user1 = User.objects.create_user(username='test_user1', password='test_user1')
        profile = Profile.objects.create(user=user1,
                                         date_of_birth=timezone.now().replace(hour=0, minute=0, second=0,
                                                                              microsecond=0))
        file_path = os.path.join(BASE_DIR, 'homepage\static\images\photo_test_profile.png')
        profile.photo = SimpleUploadedFile(name='profile_test_image.png', content=open(file_path, 'rb').read())
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.user.username, 'test_user1')
        self.assertEqual(profile.date_of_birth, timezone.now().replace(hour=0, minute=0, second=0,
                                                                       microsecond=0))
        self.assertEqual(profile.photo.name, 'profile_test_image.png')
        self.assertEqual(profile.__str__(), 'Profil użytkownika {}.'.format(user1.username))


    def test_ForumTopic_creation(self):
        user1 = User.objects.create_user(username='test_user1', password='test_user1')
        topic = ForumTopic.objects.create(author=user1, title='tytul tematu', body='tresc tematu',
                                          date_of_publication=timezone.now().replace(hour=0,minute=0, second=0, microsecond=0),
                                          slug=slugify('tytul tematu'))
        self.assertTrue(isinstance(topic, ForumTopic))
        self.assertEqual(topic.author, user1)
        self.assertEqual(topic.title, 'tytul tematu')
        self.assertEqual(topic.body, 'tresc tematu')
        self.assertEqual(topic.slug, slugify('tytul tematu'))
        self.assertEqual(topic.get_absolute_url(), '/1/tytul-tematu/')
        self.assertEqual(topic.topic_count, 1)
        self.assertEqual(topic.last_post_date.replace(minute=0, second=0, microsecond=0),
                         timezone.now().replace(minute=0, second=0, microsecond=0))
        self.assertEqual(topic.__str__(), 'tytul tematu')

    def test_ForumResponse_creation(self):
        user1 = User.objects.create_user(username='test_user1', password='test_user1')
        topic = ForumTopic.objects.create(author=user1, title='tytul tematu', body='tresc tematu',
                                          date_of_publication=timezone.now().replace(hour=0, minute=0, second=0,
                                                                                     microsecond=0),
                                          slug=slugify('tytul tematu'))
        forum_response = ForumResponse.objects.create(author=user1, body='tresc posta',
                                                      date_of_publication=timezone.now().replace(minute=0,
                                                                                                 second=0,
                                                                                                 microsecond=0),
                                                      topic=topic)

        self.assertTrue(isinstance(forum_response, ForumResponse))
        self.assertEqual(forum_response.body, 'tresc posta')
        self.assertEqual(forum_response.date_of_publication.replace(minute=0, second=0, microsecond=0), timezone.now().replace(minute=0, second=0, microsecond=0))
        self.assertEqual(forum_response.topic.title, 'tytul tematu')
        self.assertEqual(forum_response.__str__(), "Dodano post dla tematu {}".format(topic))

class Webscraper(TestCase):

    # this test works, but it is disabled to not cause unnecesary traffic on scraped webpages
    def not_test_ScraperFunction_returns_dictionary(self):
        olawa24_return_value = olawa24_scraper()
        tuolawa_return_value = tuolawa_scraper()
        kino_odra_return_value = kino_odra_scraper()
        go_kino_value = go_kino_scraper()
        um_olawa_value = um_olawa_scraper()
        self.assertTrue(isinstance(olawa24_return_value, dict))
        self.assertTrue(isinstance(tuolawa_return_value, dict))
        self.assertTrue(isinstance(kino_odra_return_value, dict))
        self.assertTrue(isinstance(go_kino_value, dict))
        self.assertTrue(isinstance(um_olawa_value, dict))

