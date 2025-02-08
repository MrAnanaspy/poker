import django
from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime

class Person(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Фамилия')
    score = models.FloatField(verbose_name='Рейтинг', default='100',)
    date_create = models.DateField(verbose_name='Дата добавления', default=django.utils.timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='Дата игры', default=django.utils.timezone.now)
    quantity = models.IntegerField(verbose_name='Количество игроков')
    avg_score = models.FloatField(verbose_name='Средний счет за столом', default='100',)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"№{self.id} - {self.date}"


class Top(models.Model):
    person = models.ForeignKey(Person, related_name='person', on_delete=models.CASCADE,
                            max_length=10, verbose_name='Игрок')
    game = models.ForeignKey(Game, related_name='game', on_delete=models.CASCADE,
                               max_length=10, verbose_name='Игра')
    place = models.IntegerField(verbose_name='Занятое место')
    price = models.IntegerField(null=True, blank=True, verbose_name='Призовые')
    score_gamer = models.FloatField(verbose_name='Очки игрока до игры', default='100',)

    def __str__(self):
        return f"{self.game}:{self.person}({self.place})"