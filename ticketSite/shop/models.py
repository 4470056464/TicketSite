from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    description=models.TextField(blank=True)
    makan=models.TextField(blank=True)
    zaman=models.TextField(blank=True)
    price=models.PositiveIntegerField()
    capacity=models.PositiveIntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('-created',)
        index_together=(('id', 'slug'),)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
