from datetime import datetime
from django.core import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Comment, Question, Answer
from .forms import CommentForm, QuestionForm, AnswerForm
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

# 질문 수정
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

# 질문 삭제
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

# 답글 수정
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    '''
    답변수정
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

# 답글 삭제
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    '''
    답글삭제
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', answer_id=answer.id)
    answer.delete()
    return redirect('pybo:index')

# 질문 댓글 작성
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    pybo 질문댓글 작성
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = datetime.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form':form}
    return render(request, 'pybo/comment_form.html', context)

# 질문 댓글 수정
@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 댓글 수정하기
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect('pybo:detail', question_id=comment.question.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = datetime.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {"form":form}
    return render(request, "pybo/comment_form.html", context)

# 질문 댓글 삭제
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 댓글 삭제하기
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect("pybo:detail", question_id=comment.question.id)
    else:
        comment.delete()
    return redirect("pybo:detail", question_id=comment.question.id)

# 답글 댓글작성
@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    답글 댓글작성
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = datetime.now()
            comment.answer = answer
            comment.save()
            return redirect("pybo:detail", question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {"form":form}
    return render(request, "pybo/comment_form.html", context)

# 답글 댓글수정
@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error("수정권한이 없습니다.")
        return redirect("pybo:detail", question_id=comment.answer.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = datetime.now()
            comment.save()
            return redirect("pybo:detail", question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {"form":form}
    return render(request, "pybo/comment_form.html", context)

# 답글 댓글삭제
@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error("삭제권한이 없습니다.")
        return redirect("pybo:detail", question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect("pybo:detail", question_id=comment.answer.question.id)

# 질문 추천
@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, "본인이 작성한 글은 추천할수 없습니다.")
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, "본인이 작성한 글은 추천할수 없습니다.")
    else:
        answer.voter.add(request.user)
    return redirect("pybo:detail", question_id=answer.question.id)