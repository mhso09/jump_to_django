from django.urls import path

from . import views

app_name='pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('question/create/', views.question_create, name='question_create'), # 질문 등록
    path('answer/create/<int:question_id>/',
         views.answer_create, name='answer_create'), # 답변 등록
    path('question/modify/<int:question_id>/',
         views.question_modify, name='question_modify'), # 질문 수정
    path('question/delete/<int:question_id>/',
         views.question_delete, name='question_delete'), # 질문 삭제
    path('answer/modify/<int:answer_id>/',
         views.answer_modify, name='answer_modify'), # 답변 수정
     path('comment/create/question/<int:question_id>', views.comment_create_question, name='comment_create_question'), #질문 댓글 등록

    path('comment/modify/question/<int:comment_id>',
         views.comment_modify_question, name='comment_modify_question'), # 질문 댓글 수정

    path('comment/delete/question/<int:comment_id>',
         views.comment_delete_question, name='comment_delete_question'), # 질문 댓글 삭제
]
