from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required

class ChineseAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用户名'
        self.fields['password'].label = '密码'

class ChineseUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用户名'
        self.fields['password1'].label = '密码'
        self.fields['password2'].label = '确认密码'
        self.fields['username'].help_text = '必填。150个字符或更少。只能包含字母、数字和@/./+/-/_。'
        self.fields['password1'].help_text = '''
            <ul>
                <li>你的密码不能与你的个人信息太相似。</li>
                <li>你的密码必须包含至少8个字符。</li>
                <li>你的密码不能是大家都爱用的常见密码。</li>
                <li>你的密码不能全部为数字。</li>
            </ul>
        '''
        self.fields['password2'].help_text = '请再次输入相同的密码进行验证。'
        
        # 添加用户档案必填字段
        self.fields['birth_date'] = forms.DateField(
            label='出生日期',
            required=True,
            widget=forms.DateInput(attrs={'type': 'date'})
        )
        self.fields['height'] = forms.IntegerField(
            label='身高(cm)',
            required=True,
            min_value=100,
            max_value=250
        )
        self.fields['weight'] = forms.FloatField(
            label='体重(kg)',
            required=True,
            min_value=30,
            max_value=200
        )
        self.fields['gender'] = forms.CharField(
            label='性别',
            required=True,
            widget=forms.Select(choices=[('M', '男'), ('F', '女'), ('O', '其他')])
        )


def register_view(request):
    if request.method == 'POST':
        form = ChineseUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 创建用户档案并保存所有必填字段
            UserProfile.objects.create(
                user=user,
                birth_date=form.cleaned_data['birth_date'],
                height=form.cleaned_data['height'],
                weight=form.cleaned_data['weight'],
                gender=form.cleaned_data['gender'],
                activity_level='M',  # 默认中等活动水平
                training_goal='MN',  # 默认保持健康
                experience_level='BG' # 默认初级
            )
            messages.success(request, '注册成功！请登录您的账号。')
            return redirect('accounts:login')
    else:
        form = ChineseUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = ChineseAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('plans:index')
            else:
                messages.error(request, '用户名或密码错误，请重试。')
    else:
        form = ChineseAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile = request.user.profile
        # 处理表单数据
        profile.gender = request.POST.get('gender')
        profile.birth_date = request.POST.get('birth_date')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.activity_level = request.POST.get('activity_level')
        profile.training_goal = request.POST.get('training_goal')
        profile.experience_level = request.POST.get('experience_level')
        profile.medical_conditions = request.POST.get('medical_conditions')
        profile.injuries = request.POST.get('injuries')
        profile.allergies = request.POST.get('allergies')
        profile.save()
        messages.success(request, '个人信息更新成功！')
        return redirect('plans:index')
    return render(request, 'accounts/profile_edit.html')
