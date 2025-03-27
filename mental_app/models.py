from django.db import models

class Teachers(models.Model):
    name = models.CharField(max_length=50)
    specialty = models.TextField()
    def __str__(self):
        return self.name


class Students(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    student = models.ManyToManyField('Teachers')

    # Поля для информации о родителе
    parent_first_name = models.CharField(max_length=50, blank=True, null=True)  # Имя родителя
    parent_last_name = models.CharField(max_length=50, blank=True, null=True)  # Фамилия родителя
    parent_phone_number = models.CharField(max_length=15, blank=True, null=True)  # Номер телефона родителя

    def __str__(self):
        return f'{self.name} {self.age} лет'
