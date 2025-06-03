from django.contrib import admin
from .models import UserProfile, Task, ClickHistory, Product, Reservation

admin.site.register(UserProfile)

class ClickHistoryInline(admin.TabularInline):
    model = ClickHistory
    extra = 0

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed')
    list_filter = ('completed',)
    inlines = [ClickHistoryInline]

admin.site.register(Task, TaskAdmin)

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            # ดึงรายการการจองทั้งหมดในระบบ
            reserved_products = Reservation.objects.values_list('product', flat=True)
            # คัดเลือกเฉพาะสินค้าที่ยังไม่มีการจอง
            kwargs["queryset"] = Product.objects.exclude(id__in=reserved_products)
        elif db_field.name == "reserved_date":
            # ดึงรายการวันที่ที่มีการจองแล้ว
            reserved_dates = Reservation.objects.values_list('reserved_date', flat=True)
            # คัดเลือกเฉพาะวันที่ที่ยังไม่มีการจอง
            kwargs["queryset"] = reserved_dates
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_by', 'created_at', 'updated_at')
    inlines = [ReservationInline]

admin.site.register(Product, ProductAdmin)
