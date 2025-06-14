from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
import json
from .models import Plan

# Create your views here.
def index(request):
    plans = Plan.objects.all()
    return render(request, 'plans/plan_select.html', {'plans': plans})

def input_rm(request):
    return render(request, 'plans/input_rm.html')

def weekly_plan(request):
    return render(request, 'plans/weekly_plan.html')
    
def ai_generator_view(request):
    """渲染AI计划生成页面"""
    return render(request, 'plans/ai_plan_generator.html')
    
@csrf_exempt
@require_http_methods(["POST"])
def generate_plan(request):
    """处理AI计划生成请求"""
    try:
        # 获取用户输入
        request_data = json.loads(request.body)
        user_message = request_data.get('message')
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # 配置API
        api_key = "sk-7c30628474f74de89dc1db404d73ef14"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建系统提示词
        system_prompt = """
        你是一名专业健身教练，请根据用户需求生成训练计划。输出格式必须为JSON：
        {
            "title": "AI智能训练计划",
            "goal": "增肌",
            "duration": 4,
            "equipment": ["哑铃"],
            "weekly_schedule": [{
                "day": "周一",
                "muscle_group": "胸部",
                "exercises": [{
                    "name": "卧推",
                    "sets": 4,
                    "reps": "8-10",
                    "rest": "90秒",
                    "description": "使用杠铃进行平板卧推"
                }]
            }],
            "notes": [
                "每周训练4天",
                "每组动作间休息60-90秒",
                "训练后补充蛋白质"
            ]
        }
        """
        
        # 调用DeepSeek API
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        response_data = response.json()
        
        # 提取并解析AI生成的计划
        ai_response = response_data['choices'][0]['message']['content']
        print("Raw AI response:", ai_response)  # 记录原始响应
        
        try:
            # 处理可能的Markdown代码块
            json_str = ai_response
            if json_str.startswith('```json') and json_str.endswith('```'):
                json_str = json_str[7:-3].strip()  # 移除```json标记
            elif json_str.startswith('```') and json_str.endswith('```'):
                json_str = json_str[3:-3].strip()  # 移除```标记
                
            # 尝试解析JSON
            plan_data = json.loads(json_str)
            
            # 验证基本字段
            required_fields = ['title', 'goal', 'weekly_schedule']
            for field in required_fields:
                if field not in plan_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # 验证周计划结构
            if not isinstance(plan_data['weekly_schedule'], list):
                raise ValueError("weekly_schedule must be an array")
                
            return JsonResponse(plan_data)
            
        except json.JSONDecodeError as e:
            print("JSON parse error:", e)
            print("Response content:", ai_response)
            return JsonResponse({
                'error': '计划解析失败',
                'details': str(e),
                'raw_response': ai_response[:500]  # 返回部分原始响应用于调试
            }, status=500)
            
        except ValueError as e:
            print("Validation error:", e)
            return JsonResponse({
                'error': '计划格式无效',
                'details': str(e),
                'raw_response': ai_response[:500]
            }, status=500)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ai_weekly_plan(request):
    """展示AI生成的周计划"""
    # 这里将从会话或URL参数中获取计划数据
    # 实际实现中需要从数据库或会话中获取计划
    sample_plan = {
        "title": "AI智能训练计划",
        "goal": "增肌",
        "duration": 4,
        "equipment": ["哑铃", "杠铃"],
        "weekly_schedule": [
            {
                "day": "周一",
                "muscle_group": "胸部",
                "exercises": [
                    {
                        "name": "卧推",
                        "sets": 4,
                        "reps": "8-10",
                        "rest": "90秒",
                        "description": "使用杠铃进行平板卧推"
                    },
                    {
                        "name": "上斜哑铃卧推",
                        "sets": 3,
                        "reps": "10-12",
                        "rest": "60秒",
                        "description": "调整凳子上斜30度"
                    }
                ]
            },
            {
                "day": "周二",
                "muscle_group": "背部",
                "exercises": [
                    {
                        "name": "引体向上",
                        "sets": 4,
                        "reps": "最大次数",
                        "rest": "90秒",
                        "description": "宽握引体向上"
                    }
                ]
            }
        ],
        "notes": [
            "每周训练4天",
            "每组动作间休息60-90秒",
            "训练后补充蛋白质"
        ]
    }
    return render(request, 'plans/ai_weekly_plan.html', {'plan': sample_plan})
