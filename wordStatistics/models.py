from django.db import models


class wordInfo(models.Model):
    word = models.CharField(max_length=100)
    count = models.BigIntegerField()

    def __str__(self):
        return '(' + self.word + ' ' + str(self.count) + ')'
