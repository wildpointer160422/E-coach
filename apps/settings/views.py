from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

@login_required
def index(request):
    return render(request, 'settings/user_setting.html')

@login_required
def user_settings(request):
    return render(request, 'settings/user_setting.html')

@login_required
@require_http_methods(["POST"])
def update_goal(request):
    try:
        data = json.loads(request.body)
        goal = data.get('goal')
        
        if not goal:
            return JsonResponse({'success': False, 'message': '未提供目标值'})
            
        # 验证目标值是否有效
        valid_goals = ['WL', 'MG', 'ST', 'EN', 'MN']
        if goal not in valid_goals:
            return JsonResponse({'success': False, 'message': '无效的目标值'})
            
        # 更新用户目标
        request.user.profile.training_goal = goal
        request.user.profile.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_http_methods(["POST"])
def update_activity_level(request):
    try:
        data = json.loads(request.body)
        activity_level = data.get('activity_level')
        
        if not activity_level:
            return JsonResponse({'success': False, 'message': '未提供活动水平值'})
            
        # 验证活动水平值是否有效
        valid_levels = ['S', 'L', 'M', 'H', 'E']
        if activity_level not in valid_levels:
            return JsonResponse({'success': False, 'message': '无效的活动水平值'})
            
        # 更新用户活动水平
        request.user.profile.activity_level = activity_level
        request.user.profile.save()
        
        return JsonResponse({'success': True, 'message': '活动水平已更新'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
