from django.contrib import admin

# Register your models here.
from apps.goods.models import GoodsImage, GoodsSKU, GoodsType
# Register your models here.


admin.site.register(GoodsType)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
