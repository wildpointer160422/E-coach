from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import StrengthTraining, CardioTraining, NutritionRecord, WaterIntake, BMRRecord
from datetime import datetime, timedelta
from django.db import models
from .utils import calculate_bmr, calculate_tdee

@login_required
def index(request):
    return redirect('nutrition:statics')

@login_required
def statics(request):
    # 获取最近7天的数据
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # 获取力量训练数据
    strength_records = StrengthTraining.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 获取有氧训练数据
    cardio_records = CardioTraining.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 获取营养摄入数据
    today = datetime.now().date()
    
    # 获取最近7天的营养记录
    nutrition_records = NutritionRecord.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 获取今日的营养记录
    today_nutrition = NutritionRecord.objects.filter(
        user=request.user,
        date=today
    ).first()
    
    nutrition_data = {
        'protein': today_nutrition.protein if today_nutrition else 0,
        'carbs': today_nutrition.carbs if today_nutrition else 0,
        'fat': today_nutrition.fat if today_nutrition else 0
    }
    
    # 计算最近7天的卡路里数据
    calorie_data = {
        'dates': [],
        'values': [],
        'bmr_values': []  # 添加BMR数据系列
    }
    
    # 使用字典临时存储每天的卡路里总和
    daily_calories = {}
    
    for record in nutrition_records:
        date_str = record.date.strftime('%m/%d')
        # 计算当天的总卡路里
        calories = (
            record.protein * 4 +  # 蛋白质：4卡路里/克
            record.carbs * 4 +    # 碳水化合物：4卡路里/克
            record.fat * 9        # 脂肪：9卡路里/克
        )
        
        # 如果这一天已经有记录，就累加
        if date_str in daily_calories:
            daily_calories[date_str] += calories
        else:
            daily_calories[date_str] = calories
    
    # 将合并后的数据按日期排序
    sorted_dates = sorted(daily_calories.keys())
    calorie_data['dates'] = sorted_dates
    calorie_data['values'] = [daily_calories[date] for date in sorted_dates]
    
    # 获取用户的基础代谢率
    bmr = calculate_bmr(request.user)
    
    # 如果尚无今日的BMR记录且能够计算BMR，则创建记录
    if bmr:
        # 获取用户资料中的体重
        profile = request.user.profile
        if profile and profile.weight:
            # 检查今天是否已有BMR记录
            today_bmr = BMRRecord.objects.filter(
                user=request.user,
                date=today
            ).first()
            
            if not today_bmr:
                # 创建新的BMR记录
                BMRRecord.objects.create(
                    user=request.user,
                    bmr_value=bmr,
                    weight=profile.weight
                )
    
    # 获取最近7天的BMR记录
    bmr_records = BMRRecord.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 为每天添加BMR值
    bmr_dict = {}
    for record in bmr_records:
        date_str = record.date.strftime('%m/%d')
        bmr_dict[date_str] = record.bmr_value
    
    # 确保所有日期都有BMR值
    for date_str in calorie_data['dates']:
        if date_str in bmr_dict:
            calorie_data['bmr_values'].append(bmr_dict[date_str])
        else:
            # 如果没有特定日期的记录，使用最新的BMR值或默认值
            latest_bmr = bmr_records.first()
            calorie_data['bmr_values'].append(latest_bmr.bmr_value if latest_bmr else (bmr or 0))
    
    # 计算今日饮水总量和记录
    today_water = WaterIntake.objects.filter(
        user=request.user,
        date=today
    )
    
    water_data = {
        'total': sum(record.amount for record in today_water),
        'records': [{
            'time': record.date.strftime('%H:%M'),
            'amount': record.amount
        } for record in today_water]
    }
    
    # 将QuerySet转换为JSON可序列化的格式
    strength_data = {
        'dates': [record.date.strftime('%m/%d') for record in strength_records],
        'squat': [record.squat for record in strength_records],
        'bench': [record.bench_press for record in strength_records],
        'deadlift': [record.deadlift for record in strength_records]
    }
    
    cardio_data = {
        'dates': [record.date.strftime('%m/%d') for record in cardio_records],
        'distance': [record.distance for record in cardio_records],
        'pace': [record.pace for record in cardio_records]
    }
    
    # 获取TDEE值（每日总能量消耗）
    tdee = calculate_tdee(request.user)
    
    # 添加用户的代谢数据
    metabolism_data = {
        'bmr': bmr,
        'tdee': tdee
    }
    
    context = {
        'strength_records': strength_data,
        'cardio_records': cardio_data,
        'nutrition_records': nutrition_data,
        'water_records': water_data,
        'calorie_data': calorie_data,
        'metabolism_data': metabolism_data,
    }
    
    return render(request, 'nutrition/statics.html', context)

@login_required
@require_POST
def record_strength(request):
    try:
        squat = float(request.POST.get('squat'))
        bench_press = float(request.POST.get('bench_press'))
        deadlift = float(request.POST.get('deadlift'))
        
        record = StrengthTraining.objects.create(
            user=request.user,
            squat=squat,
            bench_press=bench_press,
            deadlift=deadlift
        )
        
        return JsonResponse({
            'status': 'success',
            'message': '力量训练记录已保存',
            'data': {
                'date': record.date.strftime('%m/%d'),
                'squat': record.squat,
                'bench_press': record.bench_press,
                'deadlift': record.deadlift
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def record_cardio(request):
    try:
        distance = float(request.POST.get('distance'))
        pace = float(request.POST.get('pace'))
        
        record = CardioTraining.objects.create(
            user=request.user,
            distance=distance,
            pace=pace
        )
        
        return JsonResponse({
            'status': 'success',
            'message': '有氧训练记录已保存',
            'data': {
                'date': record.date.strftime('%m/%d'),
                'distance': record.distance,
                'pace': record.pace
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def record_nutrition(request):
    try:
        protein = float(request.POST.get('protein'))
        carbs = float(request.POST.get('carbs'))
        fat = float(request.POST.get('fat'))
        
        today = datetime.now().date()
        
        # 获取今日记录
        record = NutritionRecord.objects.filter(
            user=request.user,
            date=today
        ).first()
        
        if record:
            # 如果今天已有记录，更新数值
            record.protein += protein
            record.carbs += carbs
            record.fat += fat
            record.save()
        else:
            # 如果今天没有记录，创建新记录
            record = NutritionRecord.objects.create(
                user=request.user,
                date=today,
                protein=protein,
                carbs=carbs,
                fat=fat
            )
        
        return JsonResponse({
            'status': 'success',
            'message': '营养摄入记录已保存',
            'data': {
                'date': record.date.strftime('%m/%d'),
                'protein': record.protein,
                'carbs': record.carbs,
                'fat': record.fat
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def record_water(request):
    try:
        amount = int(request.POST.get('amount'))
        
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # 创建新的饮水记录
        record = WaterIntake.objects.create(
            user=request.user,
            amount=amount
        )
        
        # 计算今日总饮水量
        today_total = WaterIntake.objects.filter(
            user=request.user,
            date__range=[today_start, today_end]
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        return JsonResponse({
            'status': 'success',
            'message': '饮水记录已保存',
            'data': {
                'amount': record.amount,
                'total': today_total
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def get_bmr(request):
    """获取用户的基础代谢率数据"""
    try:
        # 计算用户的BMR
        bmr = calculate_bmr(request.user)
        tdee = calculate_tdee(request.user)
        
        if bmr is None:
            return JsonResponse({
                'status': 'error',
                'message': '无法计算BMR，请确保您已填写完整的个人信息（性别、出生日期、身高和体重）'
            }, status=400)
            
        # 获取最近7天的BMR记录
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        bmr_records = BMRRecord.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        bmr_data = {
            'current_bmr': bmr,
            'current_tdee': tdee,
            'history': [{
                'date': record.date.strftime('%Y-%m-%d'),
                'bmr': record.bmr_value,
                'weight': record.weight
            } for record in bmr_records]
        }
        
        return JsonResponse({
            'status': 'success',
            'data': bmr_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
