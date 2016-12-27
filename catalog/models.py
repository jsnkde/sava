# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models.aggregates import Count, Sum
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from sorl.thumbnail import ImageField


class AbstractClass(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Location(models.Model):
	REGIONS = (
		( 0, None),
		( 1, u"Адыгея"),
		( 2, u"Башкортостан"),
		( 3, u"Бурятия"),
		( 4, u"Алтай"),
		( 5, u"Дагестан"),
		( 6, u"Ингушетия"),
		( 7, u"Кабардино-Балкария"),
		( 8, u"Калмыкия"),
		( 9, u"Карачаево-Черкесия"),
		(10, u"Карелия"),
		(11, u"Коми"),
		(12, u"Марий Эл"),
		(13, u"Мордовия"),
		(14, u"Саха"),
		(15, u"Северная Осетия"),
		(16, u"Татарстан"),
		(17, u"Тыва"),
		(18, u"Удмуртия"),
		(19, u"Хакасия"),
		(20, u"Чечня"),
		(21, u"Чувашия"),
		(22, u"Алтайский край"),
		(23, u"Краснодарский край"),
		(24, u"Красноярский край"),
		(25, u"Приморский край"),
		(26, u"Ставропольский край"),
		(27, u"Хабаровский край"),
		(28, u"Амурская область"),
		(29, u"Архангельская область"),
		(30, u"Астраханская область"),
		(31, u"Белгородская область"),
		(32, u"Брянская область"),
		(33, u"Владимирская область"),
		(34, u"Волгоградская область"),
		(35, u"Вологодская область"),
		(36, u"Воронежская область"),
		(37, u"Ивановская область"),
		(38, u"Иркутская область"),
		(39, u"Калининградская область"),
		(40, u"Калужская область"),
		(41, u"Камчатский край"),
		(42, u"Кемеровская область"),
		(43, u"Кировская область"),
		(44, u"Костромская область"),
		(45, u"Курганская область"),
		(46, u"Курская область"),
		(47, u"Ленинградская область"),
		(48, u"Липецкая область"),
		(49, u"Магаданская область"),
		(50, u"Московская область"),
		(51, u"Мурманская область"),
		(52, u"Нижегородская область"),
		(53, u"Новгородская область"),
		(54, u"Новосибирская область"),
		(55, u"Омская область"),
		(56, u"Оренбургская область"),
		(57, u"Орловская область"),
		(58, u"Пензенская область"),
		(59, u"Пермский край"),
		(60, u"Псковская область"),
		(61, u"Ростовская область"),
		(62, u"Рязанская область"),
		(63, u"Самарская область"),
		(64, u"Саратовская область"),
		(65, u"Сахалинская область"),
		(66, u"Свердловская область"),
		(67, u"Смоленская область"),
		(68, u"Тамбовская область"),
		(69, u"Тверская область"),
		(70, u"Томская область"),
		(71, u"Тульская область"),
		(72, u"Тюменская область"),
		(73, u"Ульяновская область"),
		(74, u"Челябинская область"),
		(75, u"Забайкальский край"),
		(76, u"Ярославская область"),
		(77, u"Москва"),
		(78, u"Санкт-Петербург"),
		(79, u"Еврейская автономная область"),
		(83, u"Ненецкий автономный округ"),
		(86, u"Ханты-Мансийский автономный округ"),
		(87, u"Чукотский автономный округ"),
		(89, u"Ямало-Ненецкий автономный округ"),
		(91, u"Крым"),
		(92, u"Севастополь"),
	)

	name = models.CharField(max_length=100)
	region = models.IntegerField(choices=REGIONS)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['region', 'name']


class Karma(models.Model):
	owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owner')
	giver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='giver')
	value = models.IntegerField(default=0)

	class Meta:
		unique_together = (("owner", "giver"),)

	def __unicode__(self):
		return "{} from {}: {}".format(self.owner, self.giver, self.value)


class User(AbstractUser):
	phone = models.CharField(max_length=10, null=True, blank=True)
	location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
	karma = models.ManyToManyField('self', through='Karma', symmetrical=False)

	def phone_formatted(self):
		return "" if not self.phone or len(self.phone) != 10 else "+7 ({}{}{}) {}{}{} {}{} {}{}".format(*list(str(self.phone)))

	def __unicode__(self):
		if self.first_name and self.last_name:
			return "{} {}".format(self.first_name, self.last_name)

		else:
			return self.username

	def get_karma(self):
		return self.owner.aggregate(Sum('value'))['value__sum'] or 0

	def can_give_karma(self, usr):
		if self == usr:
			return False

		k = self.giver.filter(owner=usr)
		if not k.exists() or (k.exists() and k[0].value == 0):
			return True

		return False

	def give_karma(self, usr):
		if self == usr:
			return

		if not self.giver.filter(owner=usr).exists():
			self.giver.create(owner=usr, giver=self, value=1)

		else:
			k = self.giver.filter(owner=usr)[0]
			k.value = 1
			k.save()


	@classmethod
	def karma_all(cls):
		return cls.objects.all().annotate(karma_sum=Sum('owner__value'))


class Item(AbstractClass):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100)
	comment = models.CharField(max_length=1000, blank=True, null=True)
	active = models.BooleanField(default=True)

	tags = TaggableManager(blank=True)

	def __unicode__(self):
		return self.description[:40]


def image_upload_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.item.user.id, filename)

class Image(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	img = ImageField(upload_to=image_upload_path)

	def __unicode__(self):
		return unicode(self.img)

