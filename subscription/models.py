from django.db import models
from django.contrib.auth.models import User
from learnsync_app.models import ThesisPaper
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField()  # Duration in days or months, etc.
    features = models.TextField()

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan.name}"


class PurchaseTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(ThesisPaper, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.paper.title}"
