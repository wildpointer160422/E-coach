from datetime import date
from django.contrib.auth.models import User
from accounts.models import UserProfile

def calculate_age(birth_date):
    """根据出生日期计算年龄"""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_bmr(user):
    """
    使用米福林-圣乔尔公式计算基础代谢率
    男性: BMR = 10 × 体重(kg) + 6.25 × 身高(cm) - 5 × 年龄(岁) + 5
    女性: BMR = 10 × 体重(kg) + 6.25 × 身高(cm) - 5 × 年龄(岁) - 161
    """
    try:
        # 获取用户资料
        profile = UserProfile.objects.get(user=user)
        
        # 检查必要的数据是否存在
        if not all([profile.birth_date, profile.height, profile.weight, profile.gender]):
            return None
        
        # 计算年龄
        age = calculate_age(profile.birth_date)
        
        # 应用米福林-圣乔尔公式
        weight = profile.weight
        height = profile.height
        
        # 基础计算部分
        bmr = 10 * weight + 6.25 * height - 5 * age
        
        # 根据性别调整
        if profile.gender == 'M':  # 男性
            bmr += 5
        else:  # 女性
            bmr -= 161
            
        return round(bmr, 2)
    except UserProfile.DoesNotExist:
        return None
    except Exception as e:
        print(f"计算BMR时出错: {e}")
        return None

def get_activity_multiplier(activity_level):
    """根据活动水平返回活动因子"""
    multipliers = {
        'S': 1.2,   # 久坐（几乎不运动）
        'L': 1.375, # 轻度活动（每周运动1-3次）
        'M': 1.55,  # 中度活动（每周运动3-5次）
        'H': 1.725, # 高度活动（每周运动6-7次）
        'E': 1.9    # 专业运动员级别
    }
    return multipliers.get(activity_level, 1.2)  # 默认为久坐级别

def calculate_tdee(user):
    """计算每日总能量消耗 (TDEE) = BMR x 活动因子"""
    try:
        profile = UserProfile.objects.get(user=user)
        bmr = calculate_bmr(user)
        
        if not bmr or not profile.activity_level:
            return None
            
        activity_multiplier = get_activity_multiplier(profile.activity_level)
        tdee = bmr * activity_multiplier
        
        return round(tdee, 2)
    except Exception as e:
        print(f"计算TDEE时出错: {e}")
        return None 