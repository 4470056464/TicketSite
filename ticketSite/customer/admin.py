from django.contrib import admin
from .models import Order, OrderItem, Ticket
import csv
from django.http import HttpResponse
import datetime
def export_to_csv(modeladmin,request,queryset):
    opts=modeladmin.model._meta
    response=HttpResponse(content_type='text/csv')
    response['content-Disposition']='attachment; filename={}.csv'.format(opts.verbose_name)
    writer=csv.writer(response)

    fields=[field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field  in fields])
    for obj in queryset:
        data_row=[]
        for field in fields:
            value=getattr(obj,field.name)
            if isinstance(value,datetime.datetime):
                value=value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description='EXPORT TO CSV'


class TicketInline(admin.TabularInline):
    model = Ticket
    list_display = ('id','product', 'user')



class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone',)
    inlines = [TicketInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('quantity', 'price','order')


admin.site.register(OrderItem, OrderItemAdmin)