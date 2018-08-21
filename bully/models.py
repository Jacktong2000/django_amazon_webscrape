from django.db import models

# Create your models here.
class What_i_want(models.Model):
    item_title = models.TextField()
    item_rating = models.CharField(max_length=100)
    item_price = models.CharField(max_length=100)

    def __str__(self):
        return self.item_title
