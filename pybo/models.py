from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #작성자
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # on_delete=models.CASCADE는 유저 삭제하면 같이 삭제되도록 유도
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    # null=True는 null을 허용, blank=True는 입력 데이터 검사 시 값이 없어도 된다는 의미 
    # 즉 어떤 조건으로든 값을 비워둘 수 있음

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=CASCADE)