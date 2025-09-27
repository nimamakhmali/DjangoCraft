from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


@api_view(["GET"])
def service_reviews(request, service_id):
	# Get all reviews for a service
	reviews = Review.objects.filter(service_id=service_id).select_related('user')
	
	# Calculate average rating
	avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
	total_reviews = reviews.count()
	
	# Pagination
	page_size = int(request.GET.get('page_size', 10))
	page = int(request.GET.get('page', 1))
	
	from django.core.paginator import Paginator
	paginator = Paginator(reviews, page_size)
	page_obj = paginator.get_page(page)
	
	serializer = ReviewSerializer(page_obj, many=True)
	
	return Response({
		'results': serializer.data,
		'avg_rating': round(avg_rating, 2),
		'total_reviews': total_reviews,
		'count': paginator.count,
		'page': page,
		'num_pages': paginator.num_pages,
		'has_next': page_obj.has_next(),
		'has_previous': page_obj.has_previous(),
	})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, service_id):
	# Create a review for a service (only by buyers)
	# In a real app, you'd check if user has purchased this service
	
	# Check if user already reviewed this service
	if Review.objects.filter(service_id=service_id, user=request.user).exists():
		return Response({"detail": "You have already reviewed this service"}, status=400)
	
	serializer = ReviewCreateSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	
	review = serializer.save(service_id=service_id, user=request.user)
	return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def review_detail(request, review_id):
	try:
		review = Review.objects.get(pk=review_id)
	except Review.DoesNotExist:
		return Response({"detail": "Not found"}, status=404)
	
	# Check ownership
	if review.user != request.user:
		return Response({"detail": "Permission denied"}, status=403)
	
	if request.method == "GET":
		return Response(ReviewSerializer(review).data)
	elif request.method == "PUT":
		serializer = ReviewCreateSerializer(review, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		review = serializer.save()
		return Response(ReviewSerializer(review).data)
	elif request.method == "DELETE":
		review.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)