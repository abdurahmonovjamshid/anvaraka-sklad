from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from .models import Product


class ProductAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'highlight_total', 'get_price', 'get_total_price', 'measurement')
    list_filter = ('parent',)
    autocomplete_fields = ('parent',)
    search_fields = ('title',)

    def get_total_price(self, obj):
        if not obj.parent:
            return '-'
        formatted_price = "{:,.1f}".format(obj.total * obj.price)
        return formatted_price+'$'

    get_total_price.short_description = 'Mavjud komponent narxi'

    def get_price(self, obj):
        if not obj.parent:
            return '-'
        formatted_price = "{:,.1f}".format(obj.price)
        return formatted_price+'$'
    get_price.short_description = 'Narxi'
    get_price.admin_order_field = 'price'

    def highlight_total(self, obj):
        if obj.parent:
            if obj.total < obj.notification_limit:  # Specify your desired threshold value here
                return format_html(
                    '<span style="background-color:#FF0E0E; color:white; padding: 2px 5px;">{}</span>',
                    str(obj.total)+' '+obj.measurement
                )
            return str(obj.total)+' '+obj.measurement
        elif not obj.parent and obj.highlight:
            return format_html('<span style="background-color:#FF0E0E; color:white; padding: 2px 10px;">-</span>')

    highlight_total.short_description = 'Umumiy'
    highlight_total.admin_order_field = 'total'


admin.site.register(Product, ProductAdmin)
