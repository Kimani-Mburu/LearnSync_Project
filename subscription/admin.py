from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, PurchaseTransaction

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    list_filter = ('price', 'duration')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'start_date', 'end_date', 'active')
    list_filter = ('subscription_plan', 'active')

@admin.register(PurchaseTransaction)
class PurchaseTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper', 'timestamp', 'payment_amount')
    list_filter = ('timestamp',)
