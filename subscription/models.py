from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.DurationField()
    features = models.ManyToManyField(Feature)

    description = models.TextField()


    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan.name}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    paper = GenericForeignKey('content_type', 'object_id')
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.paper.title}"

class StripePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_intent_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - Stripe Payment - {self.amount}"

class MpesaPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_code = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - Mpesa Payment - {self.amount}"

class SubscriptionTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_timestamp = models.DateTimeField(auto_now_add=True)
    payment_gateway = models.CharField(max_length=20, choices=[('stripe', 'Stripe'), ('mpesa', 'Mpesa')])
    payment_status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan.name} - {self.transaction_id}"

class DashboardData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_purchases = models.IntegerField(default=0)
    total_stripe_payments = models.IntegerField(default=0)
    total_mpesa_payments = models.IntegerField(default=0)
    total_subscription_transactions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Dashboard Data"
