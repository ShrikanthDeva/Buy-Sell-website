from django.db import models

# Create your models here.
class product(models.Model):
    def __str__(self) -> str:
        return self.name
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    desc = models.CharField(max_length=200)
    image = models.ImageField(blank=True,upload_to='images')