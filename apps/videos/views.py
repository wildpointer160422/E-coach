from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import HealthVideo, UserVideoInteraction
import random

@login_required
def index(request):
    videos = HealthVideo.objects.all()
    return render(request, 'videos/index.html', {'videos': videos})

@login_required
def recommend_videos(request):
    # 简化版推荐算法 - 基于用户健康状况和训练目标
    user_profile = request.user.profile
    
    # 模拟视频数据 - 在实际应用中，这些数据应该来自数据库
    # 这里我们创建一些示例视频用于演示
    sample_videos = [
        {
            'id': 1,
            'title': '初学者全身力量训练',
            'description': '适合初学者的全身力量训练，无需器材，在家即可完成。',
            'video_url': 'https://www.youtube.com/embed/UBMk30rjy0o',
            'thumbnail_url': 'https://img.youtube.com/vi/UBMk30rjy0o/maxresdefault.jpg',
            'category': 'ST',
            'difficulty': 'BG',
            'duration': 20,
            'equipment_needed': '无',
            'health_conditions': '适合大多数健康状况',
        },
        {
            'id': 2,
            'title': '中级有氧运动 - 燃脂训练',
            'description': '中等强度有氧运动，帮助燃烧脂肪，提高心肺功能。',
            'video_url': 'https://www.youtube.com/embed/ml6cT4AZdqI',
            'thumbnail_url': 'https://img.youtube.com/vi/ml6cT4AZdqI/maxresdefault.jpg',
            'category': 'WT',
            'difficulty': 'IM',
            'duration': 30,
            'equipment_needed': '无',
            'health_conditions': '适合大多数健康状况',
        },
        {
            'id': 3,
            'title': '增肌训练 - 哑铃上肢锻炼',
            'description': '使用哑铃进行上肢肌肉训练，增强肌肉质量。',
            'video_url': 'https://www.youtube.com/embed/SuajkDYlIRw',
            'thumbnail_url': 'https://img.youtube.com/vi/SuajkDYlIRw/maxresdefault.jpg',
            'category': 'MG',
            'difficulty': 'IM',
            'duration': 25,
            'equipment_needed': '哑铃',
            'health_conditions': '无肩部或手腕伤病',
        },
        {
            'id': 4,
            'title': '康复训练 - 背部疼痛缓解',
            'description': '针对背部疼痛的舒缓训练，帮助缓解不适。',
            'video_url': 'https://www.youtube.com/embed/2VuLBYrgG94',
            'thumbnail_url': 'https://img.youtube.com/vi/2VuLBYrgG94/maxresdefault.jpg',
            'category': 'RC',
            'difficulty': 'BG',
            'duration': 15,
            'equipment_needed': '瑜伽垫',
            'health_conditions': '背部疼痛',
        },
        {
            'id': 5,
            'title': '高级力量训练 - 全身HIIT',
            'description': '高强度间歇训练，提高力量和耐力。',
            'video_url': 'https://www.youtube.com/embed/ml6cT4AZdqI',
            'thumbnail_url': 'https://img.youtube.com/vi/ml6cT4AZdqI/maxresdefault.jpg',
            'category': 'ST',
            'difficulty': 'AD',
            'duration': 40,
            'equipment_needed': '无',
            'health_conditions': '无心脏问题',
        },
    ]
    
    # 简单的推荐逻辑
    recommended_videos = []
    
    # 根据用户训练目标筛选视频
    if user_profile.training_goal:
        goal_map = {
            'WL': 'WT',  # 减重 -> 减重训练
            'MG': 'MG',  # 增肌 -> 增肌训练
            'ST': 'ST',  # 力量训练 -> 力量训练
            'EN': 'EN',  # 耐力训练 -> 耐力训练
            'MN': 'BG',  # 保持健康 -> 初学者指南
        }
        target_category = goal_map.get(user_profile.training_goal)
        
        # 根据训练目标筛选视频
        for video in sample_videos:
            if video['category'] == target_category:
                recommended_videos.append(video)
    
    # 如果用户有健康问题，推荐康复训练
    if user_profile.medical_conditions and '背部' in user_profile.medical_conditions:
        for video in sample_videos:
            if video['category'] == 'RC' and '背部' in video['health_conditions']:
                if video not in recommended_videos:
                    recommended_videos.append(video)
    
    # 根据用户经验水平筛选视频
    if user_profile.experience_level and recommended_videos:
        exp_map = {
            'BG': 'BG',  # 初学者 -> 初学者
            'IM': 'IM',  # 中级 -> 中级
            'AD': 'AD',  # 高级 -> 高级
        }
        target_difficulty = exp_map.get(user_profile.experience_level, 'BG')
        
        # 优先推荐符合用户经验水平的视频
        difficulty_videos = [v for v in recommended_videos if v['difficulty'] == target_difficulty]
        if difficulty_videos:
            recommended_videos = difficulty_videos
    
    # 如果没有推荐结果，返回随机视频
    if not recommended_videos:
        recommended_videos = random.sample(sample_videos, min(3, len(sample_videos)))
    
    return render(request, 'videos/recommend.html', {'videos': recommended_videos})

@login_required
def video_detail(request, video_id):
    # 在实际应用中，应该从数据库获取视频
    # 这里我们使用示例数据
    sample_videos = [
        {
            'id': 1,
            'title': '初学者全身力量训练',
            'description': '适合初学者的全身力量训练，无需器材，在家即可完成。',
            'video_url': 'https://www.youtube.com/embed/UBMk30rjy0o',
            'thumbnail_url': 'https://img.youtube.com/vi/UBMk30rjy0o/maxresdefault.jpg',
            'category': 'ST',
            'difficulty': 'BG',
            'duration': 20,
            'equipment_needed': '无',
            'health_conditions': '适合大多数健康状况',
        },
        # ... 其他视频数据 ...
    ]
    
    video = next((v for v in sample_videos if v['id'] == video_id), None)
    if not video:
        return redirect('videos:index')
    
    return render(request, 'videos/detail.html', {'video': video})

@login_required
def like_video(request, video_id):
    # 在实际应用中，应该更新数据库中的用户-视频交互记录
    return JsonResponse({'status': 'success', 'message': '已添加到喜欢的视频'})

@login_required
def save_video(request, video_id):
    # 在实际应用中，应该更新数据库中的用户-视频交互记录
    return JsonResponse({'status': 'success', 'message': '已收藏视频'})
