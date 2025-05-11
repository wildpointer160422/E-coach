from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StrengthTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strength_records')
    date = models.DateField(auto_now_add=True)
    squat = models.FloatField(verbose_name='深蹲重量(kg)')
    bench_press = models.FloatField(verbose_name='卧推重量(kg)')
    deadlift = models.FloatField(verbose_name='硬拉重量(kg)')

    class Meta:
        ordering = ['-date']
        verbose_name = '力量训练记录'
        verbose_name_plural = '力量训练记录'

class CardioTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cardio_records')
    date = models.DateField(auto_now_add=True)
    distance = models.FloatField(verbose_name='跑量(km)')
    pace = models.FloatField(verbose_name='配速(min/km)')

    class Meta:
        ordering = ['-date']
        verbose_name = '有氧训练记录'
        verbose_name_plural = '有氧训练记录'

class NutritionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_records')
    date = models.DateField()
    protein = models.FloatField(verbose_name='蛋白质(g)')
    carbs = models.FloatField(verbose_name='碳水化合物(g)')
    fat = models.FloatField(verbose_name='脂肪(g)')

    class Meta:
        ordering = ['-date']
        verbose_name = '营养摄入记录'
        verbose_name_plural = '营养摄入记录'

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_records')
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(verbose_name='饮水量(ml)')

    class Meta:
        ordering = ['-date']
        verbose_name = '饮水记录'
        verbose_name_plural = '饮水记录'

class BMRRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bmr_records')
    date = models.DateField(auto_now_add=True)
    bmr_value = models.FloatField(verbose_name='基础代谢率(kcal)')
    weight = models.FloatField(verbose_name='记录时体重(kg)')
    
    class Meta:
        ordering = ['-date']
        verbose_name = '基础代谢率记录'
        verbose_name_plural = '基础代谢率记录'
