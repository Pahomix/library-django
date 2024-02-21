from django.db import models
from django.contrib.auth.models import AbstractUser

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)
    biography = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    edition = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=50, unique=True)
    genre = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    status = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class LoanHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.book} - {self.loan_date}"
      
