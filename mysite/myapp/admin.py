from django.contrib import admin
from .models import product

# Register your models here.

admin.site.site_header = 'Buy & Sell'
admin.site.site_title = 'ABC Buying'
admin.site.index_title = 'Manage ABC Buying Websites'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','desc')
    search_fields = ('name',)

    def set_price_to_zero(self,request,queryset):
        queryset.update(price=0)
    
    actions = ('set_price_to_zero',)
    list_editable = ('price','desc')

admin.site.register(product,ProductAdmin)