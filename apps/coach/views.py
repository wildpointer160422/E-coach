from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
import json
import traceback


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
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # 配置API密钥和端点
        api_key = "sk-7c30628474f74de89dc1db404d73ef14"  # 建议将此密钥移至环境变量
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 调用DeepSeek API
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的健身健康助手，专注于提供科学、实用的运动建议和健康指导。回答要简洁专业，使用中文。"
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
