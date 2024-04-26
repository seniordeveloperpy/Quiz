from django.db import models
from django.contrib.auth.models import User

from random import sample
import string


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Quiz(CodeGenerate):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
    @property
    def all(self):
        return f'{Question.objects.filter(quiz=self.id).count()}'

class Question(CodeGenerate):
    name = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    @property
    def all_options(self):
        return Option.objects.filter(question=self)

    @property
    def correct_answer(self):
        return Option.objects.get(question=self, is_correct=True)

    @property
    def options(self):
        return Option.objects.filter(question=self)


class Option(CodeGenerate):
    name = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name},{self.question}'

    # def save(self, *args, **kwargs):
    #     options = Option.objects.filter(question=self.question).count()
    #     first = options == 0
    #     second = self.is_correct
    #     if (first and second) or (not first and not second):
    #         super(Option, self).save(*args, **kwargs)
    #     raise ValueError
    

class Answer(CodeGenerate):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_name}, {self.quiz.name}"


class AnswerDetail(CodeGenerate):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question ,on_delete=models.CASCADE)
    user_answer = models.ForeignKey(Option, on_delete=models.CASCADE)

    @property
    def is_correct(self):
        return self.user_answer == self.question.correct_answer