from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth import authenticate, login

# Create your views here.

# def signup(request):
#     """
#     계정생성
#     """
#     if request.method == "post":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password) #사용자 인증
#             login(request, user) # 로그인 하기
#             return redirect('index')
#     else:
#         form = UserForm()
#     return render(request, 'common/signup.html', {'form': form})


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('pybo:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
