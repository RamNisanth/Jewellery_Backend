from django.db import models

# Create your models here.
from accounts.models import Owner

class Jewellery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    vector_id = models.CharField(max_length=255)  # ID in vector DB
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
