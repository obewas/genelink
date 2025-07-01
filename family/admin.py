from django.contrib import admin
from .models import Person
# Register your models here.

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender')
    search_fields = ('first_name', 'last_name')

