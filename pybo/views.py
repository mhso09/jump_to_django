from datetime import datetime
from django.core import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')
    
    # 페이징처리
    paginator = Paginator(question_list, 30)  # 페이지당 30개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'question_list': page_obj}

    # context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login') # 이것이 호출되면 자동으로 로그인 화면으로 전환
def question_create(request):
    """
    pybo 질문등록
    """
    # form = QuestionForm()
    # return render(request, 'pybo/question_form.html', {'form':form})
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user #author 속성에 로그인 계정 저장
            question.create_date = datetime.now()
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')  # 이것이 호출되면 자동으로 로그인 화면으로 전환
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user #author 속성에 로그인 계정 저장
            answer.create_date = datetime.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question':question ,'form': form}
    return render(request, 'pybo/question_detail.html', context)
    

# def answer_create(request, question_id):
#     """
#     pybo 답변등록
#     """
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(content=request.POST.get(
#         'content'), create_date=timezone.now())
#     return redirect('pybo:detail', question_id=question.id)


# 또 다른 등록 방법
# def answer_create(request, question_id):
#     """
#     pybo 답변등록
#     """
#     question = get_object_or_404(Question, pk=question_id)
#     answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
#     answer.save()
#     return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''
    pybo 질문수정
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 유저와 작성자가 다를 경우
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = datetime.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    '''
    질문삭제
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    '''
    답변수정
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', answer_id=answer.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = datetime.now()
            answer.save()
            return redirect('pybo:detail', answer_id=answer.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
