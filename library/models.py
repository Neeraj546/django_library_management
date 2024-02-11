from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='created_libraries', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    libraries = models.ManyToManyField(Library, related_name='books', blank=True)
    author = models.ManyToManyField('user.User', related_name='books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='created_books', null=True, blank=True)

    def __str__(self):
        return self.title
