from django.db import models

# Create your models here.


class ExtraExpense(models.Model):
    amount = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.amount