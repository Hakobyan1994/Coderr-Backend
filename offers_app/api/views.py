from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.models import Offer,OfferDetail
from .serializer import OfferSerializer,OfferDetailSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from.permission import IsBusinessUser,IsOfferCreatorOrReadOnly
from user_auth_app.models import Profile 



class OfferListPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'

class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    pagination_class = OfferListPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator__id', 'details__delivery_time_in_days']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
      
    def get_permissions(self):
        if self.request.method == 'POST':
             return  [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()] 
      
    def get_queryset(self):
        queryset = Offer.objects.all()
        user = self.request.user
        user_profile = getattr(user, 'profile', None)
        max_delivery = self.request.query_params.get("max_delivery_time")
        if user.is_authenticated and user_profile and user_profile.user_type == 'business':
            queryset = queryset.filter(creator=user)
        if max_delivery:
            queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery)
        return queryset


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.prefetch_related('details').all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated,IsOfferCreatorOrReadOnly]
    

class OfferDetailView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer 
    permission_classes = [permissions.IsAuthenticated]   


    def perform_update(self, serializer):
        serializer.save()