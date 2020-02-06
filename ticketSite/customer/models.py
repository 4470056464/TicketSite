from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from shop.models import Product
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import pyqrcode
from pyqrcode import QRCode
import qrcode
from io import StringIO,BytesIO

class Order(models.Model):
    # code = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=200)
    # lastName = models.CharField(max_length=200)
    phone = models.IntegerField()
    national = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)



    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('ticket_pdf', args=[str(self.id)])

    def __str__(self):
        return 'Order{}'.format(self.id)


    def get_total_cost(self):
         return sum(item.get_cost() for item in self.items.all())







class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE,null=True)
    price=models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)


    def get_absolute_url(self):
        return reverse('customer.views.order_create', args=[str(self.id)])


    def get_data(self):
        return f"q{self.quantity} \n {self.order} \n p{self.product}"


    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=0,
        )
        qr.add_data(self.get_data())
        qr.make(fit=True)

        img = qr.make_image()

        buffer = BytesIO()

        img.save(buffer)
        filename = 'tickets-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png',buffer.getbuffer().nbytes, None)
        self.qrcode.save(filename, filebuffer)



