from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class HealthVideo(models.Model):
    CATEGORY_CHOICES = [
        ('ST', '力量训练'),
        ('EN', '耐力训练'),
        ('FL', '柔韧性训练'),
        ('WT', '减重训练'),
        ('MG', '增肌训练'),
        ('RC', '康复训练'),
        ('BG', '初学者指南'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('BG', '初学者'),
        ('IM', '中级'),
        ('AD', '高级'),
    ]
    
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述')
    video_url = models.URLField('视频链接')
    thumbnail_url = models.URLField('缩略图链接')
    category = models.CharField('分类', max_length=2, choices=CATEGORY_CHOICES)
    difficulty = models.CharField('难度', max_length=2, choices=DIFFICULTY_CHOICES)
    duration = models.IntegerField('时长(分钟)')
    equipment_needed = models.CharField('所需器材', max_length=200, blank=True)
    health_conditions = models.CharField('适用健康状况', max_length=200, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = '健康视频'
        verbose_name_plural = '健康视频'
        ordering = ['-created_at']


class UserVideoInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_interactions')
    video = models.ForeignKey(HealthVideo, on_delete=models.CASCADE, related_name='user_interactions')
    watched = models.BooleanField('是否观看', default=False)
    liked = models.BooleanField('是否喜欢', default=False)
    saved = models.BooleanField('是否收藏', default=False)
    watch_date = models.DateTimeField('观看时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '用户视频交互'
        verbose_name_plural = '用户视频交互'
        unique_together = ['user', 'video']
