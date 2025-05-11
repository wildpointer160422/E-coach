from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
import json
import traceback
import datetime


def index(request):
    return render(request, 'coach/ai_coach.html')


@csrf_exempt
@require_http_methods(["POST"])
def ai_coach_api(request):
    try:
        # 验证请求数据
        try:
            request_data = json.loads(request.body)
            if not isinstance(request_data, dict) or 'message' not in request_data:
                return JsonResponse({'error': 'Invalid request data format'}, status=400)
                
            user_message = request_data.get('message')
            if not user_message or not isinstance(user_message, str):
                return JsonResponse({'error': 'Message must be a non-empty string'}, status=400)
            
            share_user_data = request_data.get('share_user_data', False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # 配置API密钥和端点
        api_key = "sk-7c30628474f74de89dc1db404d73ef14"  # 建议将此密钥移至环境变量
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 准备系统提示
        system_prompt = "你是一个专业的健身健康助手，专注于提供科学、实用的运动建议和健康指导。回答要简洁专业，使用中文。"
        
        # 如果用户选择分享数据且已登录
        if share_user_data and request.user.is_authenticated:
            try:
                profile = request.user.profile
                user_data = {
                    "基本信息": {
                        "性别": profile.get_gender_display() if profile.gender else "未设置",
                        "年龄": (datetime.date.today().year - profile.birth_date.year) if profile.birth_date else "未设置",
                        "身高(cm)": profile.height,
                        "体重(kg)": profile.weight,
                        "目标体重(kg)": profile.target_weight
                    },
                    "训练情况": {
                        "活动水平": profile.get_activity_level_display() if profile.activity_level else "未设置",
                        "训练目标": profile.get_training_goal_display() if profile.training_goal else "未设置",
                        "训练经验": profile.get_experience_level_display() if profile.experience_level else "未设置"
                    },
                    "健康状况": {
                        "医疗状况": profile.medical_conditions if profile.medical_conditions else "无",
                        "受伤史": profile.injuries if profile.injuries else "无",
                        "过敏史": profile.allergies if profile.allergies else "无"
                    }
                }
                system_prompt += f"\n\n当前用户数据如下(请参考这些信息提供个性化建议):\n{json.dumps(user_data, ensure_ascii=False, indent=2)}"
            except Exception as e:
                print(f"获取用户数据失败: {str(e)}")
                traceback.print_exc()
        
        # 调用DeepSeek API
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
            "temperature": 0.7
        }
        
        # 增加重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                break
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    raise
                continue
        
        # 处理API响应
        response.raise_for_status()
        response_data = response.json()
        
        if 'choices' not in response_data or not response_data['choices']:
            return JsonResponse({'error': 'Invalid API response format'}, status=502)
            
        ai_response = response_data['choices'][0]['message']['content']
        
        return JsonResponse({'response': ai_response})
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'API request failed: {str(e)}'}, status=503)
        
    except KeyError as e:
        return JsonResponse({'error': f'Missing expected data in response: {str(e)}'}, status=502)
        
    except Exception as e:
        import logging
        logging.error('AI coach API error', exc_info=True, extra={
            'request_data': request.body.decode('utf-8')[:200],
            'error': str(e),
            'stack_trace': traceback.format_exc()
        })
        print(f"AI教练API异常: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': '服务器内部错误'}, status=500)
