import telebot
from django.contrib import admin
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

from telebot import types

from .models import Top, Person, Game

bot = telebot.TeleBot('8038800150:AAEzqdqzcXZps-GgX50GxnKAVdYos6wGqWY');


# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'score')
    readonly_fields = ['score', 'date_create']
    #list_filter = ('start_time', 'production_status', 'machine')

    @admin.display(description="Person")
    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}".upper()


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'quantity', 'avg_score', 'comment')
    readonly_fields = ['avg_score']
    list_filter = ('date', 'quantity')


@admin.register(Top)
class TopAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'game', 'place', 'price', 'score_gamer')
    readonly_fields = ['score_gamer',]
    list_filter = ('person', 'place', 'price')
    raw_id_fields = ['game', 'person']


@receiver(post_save, sender=Top)
def rating_distribution(sender, instance, created, **kwargs):
    if created:
        game = Game.objects.get(id=instance.game_id)
        person = Person.objects.get(id=instance.person_id)

        count = Top.objects.filter(game_id=game.id).count()

        instance.score_gamer = person.score

        if game.quantity <= count:
            for i in range(1, count+1):
                avg_score = 0.0
                for j in range(1, count+1):
                    if i == j:
                        continue
                    avg_score = avg_score + Person.objects.get(id=(Top.objects.get(game_id=instance.game_id, place=j)).person_id).score
                game.avg_score = (avg_score + person.score) / count+1
                game.save()
                avg_score = avg_score/(count-1)
                p = Person.objects.get(id=(Top.objects.get(game_id=instance.game_id, place=i)).person_id)
                Ea = 1 / (1 + pow(10, (avg_score-p.score)/400))
                K = 20
                if p.score > 2400:
                    K = 10
                if i==count:
                    Sa = 0
                else:
                    Sa = (1 / (count - 1)) * (count - i)
                dop_score = round((K * (Sa - Ea)), 3)
                new_score= round(p.score + dop_score, 3)
                if new_score < 0:
                    new_score = 0
                print(f"{p.first_name} {p.last_name} изменился на: {dop_score}. {p.score} --> {new_score}")
                p.score = new_score
                p.save()
        instance.save()


@receiver(post_save, sender=Person)
def add_date(sender, instance, created, **kwargs):
    if created:
        if not instance.date_create:
            instance.date_create = datetime.date.today()

@receiver(post_save, sender=Game)
def message_bot(sender, instance, created, **kwargs):
    if created:
        person = Person.objects.all()
        for p in person:
            if p.telegram_id:
                keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
                key_yes = types.InlineKeyboardButton(text='Приду', callback_data='go')  # кнопка «Да»
                keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
                key_so = types.InlineKeyboardButton(text='Приду, но опаздаю', callback_data='so')  # кнопка «Да»
                keyboard.add(key_so)  # добавляем кнопку в клавиатуру
                key_no = types.InlineKeyboardButton(text='Не приду', callback_data='stop')
                keyboard.add(key_no)
                question = 'Придешь на игру ' + str(instance) + '?'
                bot.send_message(p.telegram_id, text=question, reply_markup=keyboard)