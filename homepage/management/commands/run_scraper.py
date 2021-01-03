from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from homepage.custom_webscraper import olawa24_scraper, tuolawa_scraper, kino_odra_scraper, go_kino_scraper, um_olawa_scraper
from homepage.models import News, Movie, MovieSpectacles

class Command(BaseCommand):
    help = 'Prints all book titles in the database'

    def handle(self, *args, **kwargs):
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

        returned_dict5 = um_olawa_scraper()
        for key3 in returned_dict5:
            try:
                news3 = News.objects.get(title=key3, which_site='umolawa', date_of_publication=returned_dict5[key3]['published_date'])
            except Exception:
                news3 = News()
                news3.title = key3
                news3.link = returned_dict5[key3]['link']
                news3.date_of_publication = returned_dict5[key3]['published_date']
                news3.which_site = news3.STATUS_umolawa
                news3.content = returned_dict5[key3]['content']
                news3.save()

        returned_dict3 = kino_odra_scraper()
        for key in returned_dict3:
            compare_date = returned_dict3[key]['time_of_spectacles'][0].replace(hour=0, minute=0, second=0,
                                                                                microsecond=0)
            try:
                movie1 = Movie.objects.get(title=key, which_site='kino_odra', day_of_spectacle=compare_date)
            except:
                movie1 = Movie()
                movie1.title = key
                movie1.link = returned_dict3[key]['link']
                movie1.which_site = movie1.STATUS_kinoodra
                movie1.duration = returned_dict3[key]['duration']
                movie1.day_of_spectacle = returned_dict3[key]['time_of_spectacles'][0].replace(hour=0, minute=0,
                                                                                               second=0, microsecond=0)
                movie1.filmweb_score = returned_dict3[key]['filmweb_score']
                movie1.save()
                many_times = returned_dict3[key]['time_of_spectacles']
                for single_time in many_times:
                    try:
                        MovieSpectacles.objects.get(date=single_time,
                                                    movie_name=Movie.objects.get(title=key, which_site='kino_odra',
                                                                                 day_of_spectacle=compare_date))
                    except:
                        single_time_of_spectacle = MovieSpectacles()
                        single_time_of_spectacle.movie_name = Movie.objects.get(title=key, which_site='kino_odra',
                                                                                day_of_spectacle=compare_date)
                        single_time_of_spectacle.date = single_time
                        single_time_of_spectacle.save()

        kino_odra_movies = Movie.objects.filter(which_site='kino_odra').filter(
            day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
        kino_odra_spectacles = {}
        for one_movie in kino_odra_movies:
            dates2 = []
            for c in one_movie.all_spectacles.all():
                dates2.append(c.date.strftime('%H:%M'))
            kino_odra_spectacles[one_movie] = dates2

        returned_dict4 = go_kino_scraper()
        for key in returned_dict4:
            compare_date = returned_dict4[key]['time_of_spectacles'][0].replace(hour=0, minute=0, second=0,
                                                                                microsecond=0)
            try:
                movie2 = Movie.objects.get(title=key, which_site='gokino', day_of_spectacle=compare_date)
            except Exception:
                movie2 = Movie()
                movie2.title = key
                movie2.link = returned_dict4[key]['link']
                movie2.which_site = movie2.STATUS_gokino
                movie2.duration = returned_dict4[key]['duration']
                movie2.day_of_spectacle = returned_dict4[key]['time_of_spectacles'][0].replace(hour=0, minute=0,
                                                                                               second=0, microsecond=0)
                movie2.filmweb_score = returned_dict4[key]['filmweb_score']
                movie2.save()
                many_times = returned_dict4[key]['time_of_spectacles']
                for single_time in many_times:
                    try:
                        MovieSpectacles.objects.get(date=single_time,
                                                    movie_name=Movie.objects.get(title=key, which_site='gokino',
                                                                                 day_of_spectacle=compare_date))
                    except:
                        single_time_of_spectacle = MovieSpectacles()
                        single_time_of_spectacle.movie_name = Movie.objects.get(title=key, which_site='gokino',
                                                                                day_of_spectacle=compare_date)
                        single_time_of_spectacle.date = single_time
                        single_time_of_spectacle.save()

        gokino_movies = Movie.objects.filter(which_site='gokino').filter(
            day_of_spectacle=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
        gokino_spectacles = {}
        for one_movie in gokino_movies:
            dates1 = []
            for d in one_movie.all_spectacles.all():
                dates1.append(d.date.strftime('%H:%M'))
            gokino_spectacles[one_movie] = dates1


        # olawa24_news = News.objects.filter(which_site='olawa24').order_by('-date_of_publication')[:10]
        # tuolawa_news = News.objects.filter(which_site='tuolawa').order_by('-date_of_publication')[:10]
        # umolawa_news = News.objects.filter(which_site='umolawa').order_by('-date_of_publication')[:5]

        return "scraper finished"
