from django.contrib import admin

# Register your models here.
from .models import User, Order, Topping, Level, Decor, Berry, Shape, StandardCake, CustomCake, OrderStatistics

class CakeAdmin(admin.ModelAdmin):
    list_display = ('level', 'shape', 'topping', 'price')  # Отображаем нужные поля
    search_fields = ('level__name', 'shape__name', 'topping__name')  # Возможность поиска по полям
    filter_horizontal = ('berries', 'decor')  # Позволяет легко добавлять несколько ягод и декора



admin.site.register(User)
admin.site.register(Order)
admin.site.register(Topping)
admin.site.register(Level)
admin.site.register(Decor)
admin.site.register(Berry)
admin.site.register(Shape)
admin.site.register(CustomCake, CakeAdmin)
admin.site.register(StandardCake, CakeAdmin)
admin.site.register(OrderStatistics)