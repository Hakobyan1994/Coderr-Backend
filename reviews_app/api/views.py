from rest_framework import generics, permissions
from reviews_app.models import Review
from .serializer import ReviewSerializer
from .permissions import  IsCustomerUser

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')

        if business_user_id:
            queryset = queryset.filter(business_user__id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        ordering = self.request.query_params.get('ordering', '-updated_at')
        return queryset.order_by(ordering)

    def get_permissions(self):
        if self.request.method == 'POST':
             return  [permissions.IsAuthenticated(), IsCustomerUser()]
        elif self.request.method == 'GET':
          return [permissions.IsAuthenticated()] 


    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user) 


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]        