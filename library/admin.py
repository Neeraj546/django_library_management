from django.contrib import admin
from .models import Library, Book
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)

admin.site.register(Library, LibraryAdmin)
admin.site.register(Book, BookAdmin)

