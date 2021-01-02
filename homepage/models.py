from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField as ThumbnailImageField
from sorl.thumbnail import get_thumbnail
from django.utils.html import mark_safe
from django.urls import reverse
from django.utils.text import slugify
from tinymce import models as tinymce_models
from django.conf import settings
# Create your models here.


class News(models.Model):
    STATUS_olawa24 = 'olawa24'
    STATUS_tuolawa = 'tuolawa'
    STATUS_umolawa = 'umolawa'
    STATUS_CHOICES = (
        (STATUS_olawa24, 'Oława24'),
        (STATUS_tuolawa, 'TuOława'),
        (STATUS_umolawa, 'UMOława')
    )

    title = models.CharField(max_length=250, unique_for_month=True)
    link = models.URLField()
    which_site = models.CharField(choices=STATUS_CHOICES, default='tuolawa', max_length=10)
    date_of_publication = models.DateTimeField()
    content = models.TextField(max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "news"


class Movie(models.Model):
    STATUS_kinoodra = 'kino_odra'
    STATUS_gokino = 'gokino'
    STATUS_CHOICES = (
        (STATUS_kinoodra, 'Kino Odra'),
        (STATUS_gokino, 'GO!Kino'),
    )

    title = models.CharField(max_length=250, unique_for_month=True)
    link = models.URLField()
    which_site = models.CharField(choices=STATUS_CHOICES, default=STATUS_kinoodra, max_length=10)
    duration = models.IntegerField()
    day_of_spectacle = models.DateTimeField()
    filmweb_score = models.FloatField()

    def __str__(self):
        return self.title


class MovieSpectacles(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='all_spectacles')
    date = models.DateTimeField()

    x = str(date)

    def __str__(self):
        return self.x


class SimpleAd(models.Model):
    title = models.CharField(max_length=250)
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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/',
                                blank=True, default='default_photo.png')

    @property
    def thumbnail(self):
        if self.photo:
            return get_thumbnail(self.photo, '100x100', quality=90)

    @property
    def post_count(self):
        post_count = ForumResponse.objects.filter(author=self.user).count()
        topic_count = ForumTopic.objects.filter(author=self.user).count()
        return (post_count + topic_count)

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)


class ForumTopic(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='all_posts')
    title = models.CharField(max_length=250)
    body = tinymce_models.HTMLField()
    date_of_publication = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_of_publication')

    def get_absolute_url(self):
        return reverse('homepage:post_detail',
                       args=[self.id,
                             self.slug])

    @property
    def topic_count(self):
        current_topic = ForumTopic.objects.get(id=self.id)
        post_count = current_topic.topic_posts.all().count() + 1 # increment for topic
        return post_count

    @property
    def last_post_date(self):
        current_topic = ForumTopic.objects.get(id=self.id)
        try:
            last_post_date = current_topic.topic_posts.last().date_of_publication
        except AttributeError:
            last_post_date = current_topic.date_of_publication
        return last_post_date

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        slug = self.slug
        while True:
            try:
                test_topic = ForumTopic.objects.get(slug=slug)
                if test_topic == self:
                    self.slug = slug
                    break
                else:
                    slug = slug + '1'
            except:
                self.slug = slug
                break
        super(ForumTopic, self).save(*args, **kwargs)


class ForumResponse(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_posts')
    body = tinymce_models.HTMLField()
    date_of_publication = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(ForumTopic,
                              on_delete=models.CASCADE,
                              related_name='topic_posts')

    def __str__(self):
        return "Dodano post dla tematu {}".format(self.topic)

