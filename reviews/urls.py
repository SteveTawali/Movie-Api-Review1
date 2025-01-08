from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    MovieViewSet,
    ReviewViewSet,
    MovieListCreateView,
    MovieDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    UserUpdateView,
    UserDeleteView,
    UserListView,
    CreateMovieReviewView,
)

# Router for ViewSets
router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    # Authentication and User Profile
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-profile/', UserUpdateView.as_view(), name='update-profile'),
    path('delete-profile/', UserDeleteView.as_view(), name='delete-profile'),
    path('users/', UserListView.as_view(), name='user-list'),  # Optional

    
    # Movies
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),

    # Reviews
    path('movies/<int:movie_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('movies/<int:movie_id>/reviews/create/', CreateMovieReviewView.as_view(), name='create-movie-review'),

    # Include router URLs for ViewSets
    path('', include(router.urls)),
]