from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class MovieData(models.Model):
    title = models.CharField(max_length=250)
    year = models.SmallIntegerField()
    description = models.TextField()
    rating = models.DecimalField(max_digits = 2, decimal_places = 1, validators = [MaxValueValidator(10), MinValueValidator(0)])
    ranking = models.PositiveSmallIntegerField(validators = [MaxValueValidator(10), MinValueValidator(1)], null = True, blank = True)
    review = models.CharField(max_length=250, blank = True, null = True)
    img_url = models.URLField()
    
    def __str__(self) -> str:
        return self.title
