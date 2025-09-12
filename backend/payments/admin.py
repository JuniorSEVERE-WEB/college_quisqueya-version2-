from django.contrib import admin
from .models import EnrollmentFee, Donation, Transaction

@admin.register(EnrollmentFee)
class EnrollmentFeeAdmin(admin.ModelAdmin):
    list_display = ("student", "academic_year", "amount", "date_paid", "is_confirmed")
    list_filter = ("is_confirmed", "academic_year")
    search_fields = ("student__username", "student__email")


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("donor", "name", "amount", "date_donated")
    search_fields = ("name", "email")
    list_filter = ("date_donated",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_type", "amount", "date", "status")
    list_filter = ("payment_type", "status", "date")
    search_fields = ("user__username", "user__email")
