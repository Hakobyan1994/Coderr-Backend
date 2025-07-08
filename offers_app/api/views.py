from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.models import Offer,OfferDetail
from .serializer import OfferSerializer,OfferDetailSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from.permission import IsBusinessUser,IsOfferCreatorOrReadOnly
from user_auth_app.models import Profile 
from django.db.models import Prefetch,Q
from rest_framework.exceptions import ValidationError

class OfferListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 6                      
    page_size_query_param = "page_size"  
    max_page_size = 100

class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    pagination_class = OfferListPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator__id', 'details__delivery_time_in_days',]
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
     user_profile = getattr(user, "profile", None)
     offer_filters   = Q()
     detail_filters  = Q()

     if user.is_authenticated and user_profile and user_profile.user_type == "business":
        offer_filters &= Q(creator=user)

     min_price = self.request.query_params.get("min_price")
     if min_price:
        try:
            min_price = float(min_price)
            offer_filters   &= Q(details__price__gte=min_price)
            detail_filters  &= Q(price__gte=min_price)
        except ValueError:
            raise ValidationError({"min_price": "Nur Zahlen sind erlaubt."})                                          

     max_delivery_time = self.request.query_params.get("max_delivery_time")
     if max_delivery_time:
        try:
            max_delivery_time = int(max_delivery_time)
            offer_filters   &= Q(details__delivery_time_in_days__lte=max_delivery_time)
            detail_filters  &= Q(delivery_time_in_days__lte=max_delivery_time)
        except ValueError:
            raise ValidationError({"max_delivery_time": "Nur ganze Zahlen sind erlaubt."})

     queryset = queryset.filter(offer_filters).distinct()

     if detail_filters:
        detail_qs = OfferDetail.objects.filter(detail_filters)
     else:
        detail_qs = OfferDetail.objects.all()

     queryset = queryset.prefetch_related(Prefetch("details", queryset=detail_qs))

     return queryset


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
              return [permissions.IsAuthenticated(),IsOfferCreatorOrReadOnly()]  
        return [permissions.IsAuthenticated()]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["is_detail"] = True 
        return ctx

    def get_object(self):
        pk = self.kwargs['pk']
        detail = OfferDetail.objects.filter(pk=pk).select_related('offer').first()
        if detail:
            offer = (
                Offer.objects
                .filter(pk=detail.offer_id)
                .prefetch_related(
                    Prefetch('details',
                             queryset=OfferDetail.objects.filter(pk=pk))
                )
                .get()  
            )
            self.check_object_permissions(self.request, offer)
            return offer
        offer = get_object_or_404(Offer.objects.prefetch_related('details'), pk=pk)
        self.check_object_permissions(self.request, offer)
        return offer


class OfferDetailView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer 
    permission_classes = [permissions.IsAuthenticated]   

    def perform_update(self, serializer):
        serializer.save()