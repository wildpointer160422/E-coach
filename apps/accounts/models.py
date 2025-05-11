from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女')
    ]
    
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    ACTIVITY_LEVEL_CHOICES = [
        ('S', '久坐（几乎不运动）'),
        ('L', '轻度活动（每周运动1-3次）'),
        ('M', '中度活动（每周运动3-5次）'),
        ('H', '高度活动（每周运动6-7次）'),
        ('E', '专业运动员级别')
    ]

    GOAL_CHOICES = [
        ('WL', '减重'),
        ('MG', '增肌'),
        ('ST', '力量训练'),
        ('EN', '耐力训练'),
        ('MN', '保持健康')
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('BG', '初学者'),
        ('IM', '中级'),
        ('AD', '高级')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 基本信息
    birth_date = models.DateField('出生日期', null=True, blank=True)
    height = models.FloatField('身高(cm)', validators=[MinValueValidator(100), MaxValueValidator(250)], null=True, blank=True)
    weight = models.FloatField('体重(kg)', validators=[MinValueValidator(30), MaxValueValidator(200)], null=True, blank=True)
    
    # 健康和训练相关
    activity_level = models.CharField('活动水平', max_length=1, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True)
    training_goal = models.CharField('训练目标', max_length=2, choices=GOAL_CHOICES, null=True, blank=True)
    experience_level = models.CharField('训练经验', max_length=2, choices=EXPERIENCE_LEVEL_CHOICES, null=True, blank=True)
    target_weight = models.FloatField('目标体重(kg)', null=True, blank=True)
    daily_calorie_goal = models.IntegerField('每日卡路里目标', null=True, blank=True)
    
    # 健康状况
    medical_conditions = models.TextField('健康状况', blank=True)
    injuries = models.TextField('受伤史', blank=True)
    allergies = models.TextField('过敏史', blank=True)
    
    # 会员相关
    is_premium = models.BooleanField('是否为会员', default=False)
    premium_expiry = models.DateField('会员到期日期', null=True, blank=True)
    
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return f"{self.user.username}的个人档案"

    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'

class ProgressRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    record_date = models.DateField('记录日期', auto_now_add=True)
    weight = models.FloatField('体重(kg)', validators=[MinValueValidator(30), MaxValueValidator(200)])
    body_fat = models.FloatField('体脂率(%)', null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    muscle_mass = models.FloatField('肌肉量(kg)', null=True, blank=True)
    notes = models.TextField('备注', blank=True)
    
    class Meta:
        verbose_name = '进度记录'
        verbose_name_plural = '进度记录'
        ordering = ['-record_date']

class TrainingSession(models.Model):
    COMPLETION_STATUS_CHOICES = [
        ('C', '已完成'),
        ('P', '部分完成'),
        ('S', '跳过'),
        ('F', '未完成')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_sessions')
    date = models.DateField('训练日期')
    duration = models.IntegerField('训练时长(分钟)')
    calories_burned = models.IntegerField('消耗卡路里', null=True, blank=True)
    perceived_intensity = models.IntegerField('感知强度(1-10)', 
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    completion_status = models.CharField('完成状态', max_length=1, choices=COMPLETION_STATUS_CHOICES)
    notes = models.TextField('训练笔记', blank=True)
    
    class Meta:
        verbose_name = '训练记录'
        verbose_name_plural = '训练记录'
        ordering = ['-date']

class UserGoalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goal_history')
    goal_type = models.CharField('目标类型', max_length=2, choices=UserProfile.GOAL_CHOICES)
    start_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期', null=True, blank=True)
    target_value = models.FloatField('目标值', null=True, blank=True)
    achieved = models.BooleanField('是否达成', default=False)
    notes = models.TextField('备注', blank=True)
    
    class Meta:
        verbose_name = '目标历史'
        verbose_name_plural = '目标历史'
        ordering = ['-start_date']
