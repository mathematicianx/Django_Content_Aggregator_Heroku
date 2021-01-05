from django.db import models


class KinoOdraMoviesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(which_site='kino_odra')

class GoKinoMoviesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(which_site='gokino')

class Olawa24NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(which_site='olawa24')

class TuOlawaNewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(which_site='tuolawa')

class UMOlawaNewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(which_site='umolawa')
