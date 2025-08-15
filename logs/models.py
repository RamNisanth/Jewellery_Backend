from django.db import models

# Create your models here.
from accounts.models import Customer

class Log(models.Model):
    id = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    category = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id.name} - {self.category} - {self.count}"
