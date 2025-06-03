from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class ClickHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    clicked_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('', '-------'), ('proceed', 'ดำเนินการ'), ('success', 'เสร็จสิ้น')], blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.name} - {self.clicked_date}"

class Task(models.Model):
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # เพิ่มการเชื่อมโยงกับ Product
    reserved_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.reserved_date}"
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_leader', blank=True)
    members = models.ManyToManyField(User, through='Member', related_name='group_members')

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_memberships')
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'