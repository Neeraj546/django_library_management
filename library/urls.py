from django.urls import path
from .views.author_views import ListAuthors
from .views.library_views import ListLibraryView, CreateLibraryView
from .views.book_views import ListBookView, CreateBookView

urlpatterns = [
    path('authors/', ListAuthors.as_view(), name='author-list'),
    path('list/', ListLibraryView.as_view(), name='libraries'),
    path('create/', CreateLibraryView.as_view(), name='create-library'),
    path('<int:id>/update/', CreateLibraryView.as_view(), name='update-library'),
    path('<int:id>/delete/', CreateLibraryView.as_view(), name='delete-library'),
    path('books/', ListBookView.as_view(), name='books'),
    path('books/create/', CreateBookView.as_view(), name='create-book'),
    path('books/<int:id>/update/', CreateBookView.as_view(), name='update-book'),
    path('books/<int:id>/delete/', CreateBookView.as_view(), name='delete-book'),
]