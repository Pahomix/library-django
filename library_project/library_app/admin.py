from django.contrib import admin
from . models import Author, Book, LoanHistory, CustomUser

# Register your models here.

class AuthorAdmin (admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)

class BookAdmin (admin.ModelAdmin):
  list_display = ('title', 'author', 'edition', 'genre', 'publication_year', 'status')
admin.site.register(Book, BookAdmin)

class LoanHistoryAdmin (admin.ModelAdmin):
  list_display = ('user', 'book', 'loan_date', 'return_date')
admin.site.register(LoanHistory, LoanHistoryAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_password_display', 'role')

    def get_password_display(self, obj):
        return obj.password

    get_password_display.short_description = 'Password'

  
admin.site.register(CustomUser, UserAdmin)
  