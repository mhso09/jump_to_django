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
]
