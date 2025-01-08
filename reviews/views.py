from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import Movie, Review
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    MovieSerializer,
    ReviewSerializer,
)

# Custom Pagination
class ReviewPagination(PageNumberPagination):
    page_size = 10  # Adjust page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100  # Adjust max size if needed

# Review ViewSet for CRUD operations and sorting
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication for any review action
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['movie__title', 'rating']  # Search by movie title
    ordering_fields = ['created_at', 'rating']  # Allow sorting by rating or creation date
    pagination_class = ReviewPagination  # Add pagination to review list

    def get_queryset(self):
        queryset = Review.objects.all()
        movie_title = self.request.query_params.get('movie_title', None)
        rating = self.request.query_params.get('rating', None)

        if movie_title:
            queryset = queryset.filter(movie__title__icontains=movie_title)  # Filter by movie title
        
        if rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    queryset = queryset.filter(rating=rating)  # Filter by rating
                else:
                    return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid rating value. Rating must be an integer between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        
        return queryset


# Movie ViewSet for CRUD operations and search
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication for any movie action
    filter_backends = [SearchFilter]
    search_fields = ['title', 'genre']  # Search by movie title and genre


# Registration view
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to register (no authentication required)

    def post(self, request):
        data = request.data
        
        if "username" not in data or "password" not in data:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),  # Ensure password is hashed
            email=data.get("email", ""),
        )
        
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


# Login view with JWT token generation
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to log in (no authentication required)
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)}
            )
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Movie management views (List, Detail, Create, Update, Delete)
class MovieListCreateView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        movie.delete()
        return Response({"message": "Movie deleted successfully"})


# Review management with optional search by Movie Title and Rating filtering
class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        movie_title = request.query_params.get('movie_title', None)
        rating = request.query_params.get('rating', None)

        # Filter by movie title if provided
        if movie_title:
            reviews = reviews.filter(movie__title__icontains=movie_title)

        # Filter by rating if provided
        if rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    reviews = reviews.filter(rating=rating)
                else:
                    return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid rating value. Rating must be an integer between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the filtered reviews
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, movie_id):
        # Check if the movie exists
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the movie_id to the request data before saving the review
        data = request.data
        data['movie'] = movie.id  # Attach the movie to the review

        # Serialize and save the review
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
        # Apply pagination
        paginator = ReviewPagination()
        result_page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, movie_id):
        data = request.data
        data["movie"] = movie_id
        data["user"] = request.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Review Detail View (Edit/Delete Review)
class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication to edit/delete reviews

    def put(self, request, review_id):
        review = Review.objects.get(id=review_id, user=request.user)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = Review.objects.get(id=review_id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted successfully"})
    

# User Profile view
class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication to view profile