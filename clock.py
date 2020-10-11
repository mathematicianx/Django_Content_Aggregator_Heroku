from apscheduler.schedulers.blocking import BlockingScheduler

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
import re
from selenium.webdriver.firefox.options import Options
from requests_html import HTMLSession
from filmweb.filmweb import Filmweb
import os
from django.utils import timezone
from .models import News, Movie, MovieSpectacles


def olawa24_scraper():
    """
    This is a scraper for news from Olawa24.pl website
    :return: Dictionary where:
                    keys = news title
                    values= {
                            link: full_link,
                            date: date,
                            }
    """
    url = "https://olawa24.pl/wiadomosci"
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    soup = BeautifulSoup(html, 'lxml')  # had to change parser to work
    all_news = soup.find_all("li", class_='c-news-list__item c-news-list-item')
    full_link, title, date = '', '', ''  # default value in case something goes wrong
    returned_dict = {}
    for single_news in all_news:
        divs = single_news('div')
        for div in divs:
            try:
                full_link = 'https://olawa24.pl' + div.find('a', class_='c-news-list-item__link')['href']
                title = div.find('img')['alt']
            except (TypeError, AttributeError):
                pass
            try:
                x = div.find(class_='c-news-list-item__date').text
                date = datetime.strptime(x,  "%Y-%m-%d %H:%M:%S")
            except AttributeError:
                pass
        returned_dict[title] = {'link': full_link,
                                'date': date,
                                }
    return returned_dict


def today_yesterday_two_days_ago(input_string):
    """
    This is used for converting "Today, %H:%M", "Yesterday, %H:%M" and "2 Days ago, %H:%M" to datetime.
    :param input_string: String scraped from web with badly formatted date
    :return: datetime object
    """
    short_pattern = re.compile(r'(\d\d): ?(\d\d)')
    long_pattern = re.compile(r'(\d\d.\d\d.\d\d\d\d, \d\d:) ?(\d\d)')
    dt_object = '1990-09-01 00:00:00'  # set default value if not found
    test_cnd = ['Dzisiaj', 'Wczoraj', '2 dni temu']  # special cases for which we search
    for test in test_cnd:
        if test in input_string:
            tmp_index = test_cnd.index(test)  # define which special case is found
            dt_object = datetime.today() - timedelta(tmp_index)
            # from today remove 0 days, 1 day, 2 days based on index
            if short_pattern.search(input_string) is None:
                # even if special case exists, the hours:minutes can be formatted badly that's why we check here
                hours = 0  # default values
                minutes = 0
            else:
                hours = int(short_pattern.search(input_string).group(1))
                minutes = int(short_pattern.search(input_string).group(2))
            dt_object = dt_object.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        try:
            x = long_pattern.search(input_string).group(1) + long_pattern.search(input_string).group(2)
            dt_object = datetime.strptime(x, "%d.%m.%Y, %H:%M")
        except AttributeError:
            pass
    return dt_object


def tuolawa_scraper():
    """
    This is a scraper for news from TuOława.pl website
    :return: Dictionary where:
                    keys = news title
                    values= {
                            link: full_link,
                            date: date,
                            }
    """
    url = "https://www.tuolawa.pl/wiadomosci/192/aktualnosci"
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    returned_dict = {}
    results = soup.find_all("div", class_="articles_list_item")
    for result in results:
        try:
            title = result.a['title']
            link = result.a['href']
            incorrect_dt_format = result.find(class_="text-muted").text.lstrip('\n')
            correct_dt_format = today_yesterday_two_days_ago(incorrect_dt_format)
            date1 = correct_dt_format
        except (TypeError, AttributeError):
            continue
        returned_dict[title] = {'link': link,
                                'date': date1,
                                }
    return returned_dict


def kino_odra_scraper():
    """
    This is a scraper for movie titles which premiere in Kino Odra
    :return: Dictionary where:
                    keys = movie title
                    values= {
                            'link': full_link,
                            'duration': duration,
                            'time_of_spectacles': [time_of_spectacles,]
                            }
    """
    url = "http://kultura.olawa.pl/kino/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='movie-info-container')
    returned_dict = {}
    for result in results:  # iterating throught movies
        time_of_spectacles = []  # this is reset for each new movie
        link = result.a['href']
        title = result.a.text
        returned_dict[result.a.text] = result.a['href']
        duration = result.find('span', class_='movie-time').text.lstrip().rstrip('\'')
        tmp_time_of_spctcl = result.find_all('span', class_='movie-hour')
        fw = Filmweb()
        filmweb_score = fw.search(title)[0].get_info()['rate']
        for one_tmp_time in tmp_time_of_spctcl:
            hours = int(one_tmp_time.text[:2])
            minutes = int(one_tmp_time.text[3:])
            x = timezone.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)
            time_of_spectacles.append(x)
        returned_dict[title] = {
            'link': link,
            'duration': duration,
            'time_of_spectacles': time_of_spectacles,
            'filmweb_score': filmweb_score
        }
    return returned_dict


def go_kino_scraper():
    """
    This is a scraper for movie titles which premiere in GO!Kino
    :return: Dictionary where:
                    keys = movie title
                    values= {
                            'link': full_link,
                            'duration': duration,
                            'time_of_spectacles': [time_of_spectacles <----datetime object]
                            }
    """
    pattern1 = re.compile(r'\d{2}|\d{3}')


    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options)
    #                            #executable_path=r'C:\Users\gora-pc\AppData\Local\Programs\Python\Python38-32\Scripts\geckodriver.exe')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    session = HTMLSession()
    url = "https://gokino.pl/olawa/repertuar/"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='item ng-scope')
    returned_dict = {}
    for result in results:
        first_container = result.find('div', class_='col-xs-12 col-md-8 hidden-md-down')
        second_container = result.find('div', class_='col-md-4 hidden-sm-down hours text-xs-center')
        title = first_container.h4.text
        link = 'https://gokino.pl' + first_container.a['href']
        duration_bad_format = result.find('p', class_='ng-binding').text.split('\n')[0]
        # this returns long string separated with \n. 0 element is duration
        if pattern1.search(duration_bad_format) is not None:
            duration = int(pattern1.search(duration_bad_format).group())
        else:
            duration = 0
        spectacles = second_container.find_all('div', class_='col-md-3 ng-scope')
        time_of_spectacles = []
        fw = Filmweb()
        filmweb_score = fw.search(title)[0].get_info()['rate']
        for spec in spectacles:
            hours = int(spec.text.lstrip('\n').rstrip()[:2])
            minutes = int(spec.text.lstrip('\n').rstrip()[3:])
            x = timezone.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)
            time_of_spectacles.append(x)
        returned_dict[title] = {'link': link,
                                'duration': duration,
                                'time_of_spectacles': time_of_spectacles,
                                'filmweb_score': filmweb_score}
    driver.close()
    return returned_dict
go_kino_scraper()

def um_olawa_scraper():
    main_url = 'https://www.um.olawa.pl/?start='
    headers = {'User-Agent': 'Mozilla/5.0'}
    returned_dict = {}
    for i in range(0, 15, 5):
        real_url = main_url + str(i)
        request = Request(real_url, headers=headers)
        html = urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')
        result_from_single_page = soup.find_all('div', class_='item column-1')
        for result in result_from_single_page:
            title = result.find(class_='page-header').h2.a.text.strip()
            content = result.find(class_='intro-article')
            if content.p is not None:
                content = content.p.text
            else:
                content = 'Brak Zawartości'
            link = 'https://www.um.olawa.pl/' + result.find(class_='page-header').h2.a['href']
            raw_published_date = result.find('time')['datetime']
            overall_date = raw_published_date[0:10]
            detail_date = raw_published_date[11:19]
            published_date = datetime.strptime(overall_date + ' ' +detail_date, '%Y-%m-%d %H:%M:%S')
            if title not in returned_dict:
                returned_dict[title] = {'content': content,
                                        'link': link,
                                        'published_date': published_date}
            else:
                title = title + '1'
                returned_dict[title] = {'content': content,
                                        'link': link,
                                        'published_date': published_date}
    return returned_dict


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


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=30)
def timed_job():
    save_data_from_scrapers()

sched.start()
