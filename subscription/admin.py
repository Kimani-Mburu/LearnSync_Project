from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Purchase, StripePayment, MpesaPayment, SubscriptionTransaction, DashboardData, Feature

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    search_fields = ('name',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'start_date', 'end_date')
    list_filter = ('subscription_plan', 'start_date', 'end_date')
    search_fields = ('user__username', 'subscription_plan__name')

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper', 'purchased_at')
    list_filter = ('purchased_at',)
    search_fields = ('user__username', 'paper__title')

class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('user__username',)

class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('user__username',)

class SubscriptionTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'transaction_id', 'transaction_amount', 'payment_gateway', 'payment_status')
    list_filter = ('payment_gateway', 'payment_status')
    search_fields = ('user__username', 'subscription_plan__name', 'transaction_id')

class DashboardDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_purchases', 'total_stripe_payments', 'total_mpesa_payments', 'total_subscription_transactions')
    search_fields = ('user__username',)

admin.site.register(Feature, FeatureAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(StripePayment, StripePaymentAdmin)
admin.site.register(MpesaPayment, MpesaPaymentAdmin)
admin.site.register(SubscriptionTransaction, SubscriptionTransactionAdmin)
admin.site.register(DashboardData, DashboardDataAdmin)
