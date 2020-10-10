from django.contrib import admin
#
# # Register your models here.
from .models import FoundGoods, Catalog


@admin.register(FoundGoods)
class FoundGoodsAdmin(admin.ModelAdmin):
    list_display = ['user', 'bar_code', 'lm_code', 'caption', 'amount_goods', 'create_at', 'update_at', 'note_add',
                    'shop_num']
    fields = ['user', 'bar_code', 'lm_code', 'caption', 'amount_goods', 'note_add', 'create_at', 'update_at',
              'shop_num']
    list_display_links = ('bar_code', 'lm_code', 'caption')
    search_fields = ('bar_code', 'lm_code',)
    readonly_fields = ('create_at',)
    list_editable = ('note_add', 'amount_goods',)
    list_filter = ('create_at', 'update_at', 'shop_num')
    save_as = True
    # save_on_top = True


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'ean', 'lm', 'product_name']
    fields = ('ean', 'lm', 'name_product')
    search_fields = ('ean', 'lm', 'product_name',)
