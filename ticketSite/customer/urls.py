from django.conf.urls import url, include
from . import views
from django.urls import path
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
   path('create/', views.order_create, name='order_create'),
   path('create/pdf',views.pdf_ticket, name='pdf'),
   # path('reserve/<int:product_id>', views.reserve_ticket, name='reserve_ticket'),
   path('create/<int:order_id>', views.ticket_pdf.as_view(),name='ticket_pdf')

]
