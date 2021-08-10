from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class BusinessDetail(models.Model):
    """Model definition for Proj."""
    Name = models.CharField(verbose_name='Project Name',
                            max_length=100, null=True)
    logo = models.ImageField(
        verbose_name='Logo', upload_to='static/image/logo/', null=True)
    
    # theme=models.BooleanField(default=False)

    def __str__(self):
        return self.Name


