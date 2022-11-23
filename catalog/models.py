from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    account = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=12, default=None, null=True)
    email = models.CharField(max_length=100, default=None, null=True)
    confirm_string = models.CharField(max_length=256, default=None, null=True)
    code = models.CharField(max_length=6, default=None, null=True)
    must_change_password = models.BooleanField(default=False)
    badge = models.IntegerField(default=0)
    fb_id = models.IntegerField(default=0)
    privacy_policy = models.BooleanField(default=False)

    class Meta:
        ordering = ['id', 'account', 'email', 'phone']


class UserSet(models.Model):
    user = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE, related_name='set_user')
    name = models.CharField(max_length=256, default=None, null=True)
    birthday = models.CharField(max_length=256, null=True, default=None)
    height = models.FloatField(max_length=256, null=True, default=None)
    gender = models.BooleanField(default=False)
    fcm_id = models.CharField(max_length=256, null=True, default=None)
    address = models.CharField(max_length=256, null=True, default=None)
    weight = models.CharField(max_length=256, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user']


class Pressure(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='pressure')
    systolic = models.FloatField(max_length=256, null=True)
    diastolic = models.FloatField(max_length=256, null=True)
    pulse = models.IntegerField(null=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id', 'user', 'recorded_at']


class Weight(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='weight')
    weight = models.FloatField(max_length=256, null=True)
    body_fat = models.FloatField(max_length=256, null=True)
    bmi = models.FloatField(max_length=256, null=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id', 'user', 'recorded_at']


class Sugar(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='sugar')
    sugar = models.IntegerField(null=True)
    time_period = models.IntegerField(null=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id', 'user', 'recorded_at']


class A1c(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='a1c')
    a1c = models.FloatField(max_length=256, null=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id', 'user', 'recorded_at']


class Default(models.Model):
    user = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE, related_name='default')
    sugar_delta_max = models.IntegerField(null=True, default=None)
    sugar_delta_min = models.IntegerField(null=True, default=None)
    sugar_morning_max = models.IntegerField(null=True, default=None)
    sugar_morning_min = models.IntegerField(null=True, default=None)
    sugar_evening_max = models.IntegerField(null=True, default=None)
    sugar_evening_min = models.IntegerField(null=True, default=None)
    sugar_before_max = models.IntegerField(null=True, default=None)
    sugar_before_min = models.IntegerField(null=True, default=None)
    sugar_after_max = models.IntegerField(null=True, default=None)
    sugar_after_min = models.IntegerField(null=True, default=None)
    systolic_max = models.IntegerField(null=True, default=None)
    systolic_min = models.IntegerField(null=True, default=None)
    diastolic_max = models.IntegerField(null=True, default=None)
    diastolic_min = models.IntegerField(null=True, default=None)
    pulse_max = models.IntegerField(null=True, default=None)
    pulse_min = models.IntegerField(null=True, default=None)
    weight_max = models.IntegerField(null=True, default=None)
    weight_min = models.IntegerField(null=True, default=None)
    bmi_max = models.IntegerField(null=True, default=None)
    bmi_min = models.IntegerField(null=True, default=None)
    body_fat_max = models.IntegerField(null=True, default=None)
    body_fat_min = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id', 'user']


class UserSetting(models.Model):
    user = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE, related_name='setting')
    after_recording = models.BooleanField(default=False)
    no_recording_for_a_day = models.BooleanField(default=False)
    over_max_or_under_min = models.BooleanField(default=False)
    after_meal = models.BooleanField(default=False)
    unit_of_sugar = models.BooleanField(default=False)
    unit_of_weight = models.BooleanField(default=False)
    unit_of_height = models.BooleanField(default=False)

    class Meta:
        ordering = ['id', 'user']


class Diet(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='diet')
    description = models.TextField(null=True, default=None, blank=True)
    meal = models.IntegerField(null=True, default=None)
    tag = models.JSONField(null=True, blank=True)
    image = models.IntegerField(default=0)
    lat = models.FloatField(max_length=256, null=True)
    lng = models.FloatField(max_length=256, null=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id', 'user', 'recorded_at']


class Medical(models.Model):
    user = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE, related_name='medical')
    diabetes_typ = models.IntegerField(null=True, default=None)
    oad = models.BooleanField(default=False)
    insulin = models.BooleanField(default=False)
    anti_hypertensives = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id', 'user']


class Drug(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='drug')
    type = models.BooleanField(default=False)
    name = models.CharField(max_length=256, null=True, default=None)
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['id', 'user', 'recorded_at']


class Friend(models.Model):
    inviter = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='code_1')
    invitees = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='code_2')
    type = models.IntegerField(default=None)
    accept = models.IntegerField(default=0)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['type', 'inviter', 'invitees']


class Care(models.Model):
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='care')
    member_id = models.IntegerField(default=0)
    reply_id = models.IntegerField(default=0)
    message = models.TextField(
        max_length=1000, help_text='關懷諮詢')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']
