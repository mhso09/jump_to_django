from django.contrib import admin
from .models import Question

# 검색기능 추가하기
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)