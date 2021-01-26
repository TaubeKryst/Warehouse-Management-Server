from django.db import models
from django.core.validators import MinValueValidator
from rest_framework.reverse import reverse


class Product(models.Model):
    manufacturer_name = models.CharField(max_length=400)
    model_name = models.CharField(max_length=40)
    price = models.CharField(max_length=10)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def get_api_url(self, request=None):
        return reverse("api-products:post-rud", kwargs={'pk': self.pk}, request=request)
