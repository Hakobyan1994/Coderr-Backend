from .permission import IsCustomerUser
from orders_app.models import  Order
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializer import ListCreateOrderSerializer,SingleOrderSerializer
from django.db.models import Q
from offers_app.api.permission import IsBusinessUser
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from user_auth_app.models import Profile
from rest_framework.response import Response

class ListCreateOrderView(generics.ListCreateAPIView):
    serializer_class = ListCreateOrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user)).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsCustomerUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    


class  SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class=SingleOrderSerializer   



    def get_permissions(self):
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsBusinessUser]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

    def perform_update(self, serializer):
        serializer.save()



class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id,):
        # User über die URL-ID holen
        business_user = get_object_or_404(User, id=business_user_id)
        profile = get_object_or_404(Profile, user=business_user)

        if profile.user_type != 'business':
            return Response(
                {"error": "User is not a business user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_count = Order.objects.filter(
            business_user=business_user, 
            status='in_progress'
        ).count()

        return Response({"order_count": order_count}, status=status.HTTP_200_OK)
    


class CompletedOrderCountView(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request,business_user_id):
          business_user=get_object_or_404(User,id=business_user_id)  
          profile=get_object_or_404(Profile,user=business_user)
          if profile.user_type != 'business':
            return Response(
                {"error": "User is not a business user."},
                status=status.HTTP_400_BAD_REQUEST
            )
          completed_orders=Order.objects.filter(business_user=business_user,status='completed').count()
          return Response({'completed_order_count': completed_orders}, status=status.HTTP_200_OK)
            


