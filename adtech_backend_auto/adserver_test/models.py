from __future__ import unicode_literals

from django.db import models

# Create your models here.
class test_result(models.Model):
	date = models.IntegerField()
	name = models.TextField()
	data = models.TextField()