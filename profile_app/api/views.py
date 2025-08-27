from rest_framework import generics, permissions
from profile_app.models import BusinessProfile, CustomerProfile
from .serializer import BusinessProfileSerializer, CustomerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from user_auth_app.models import Profile
from rest_framework.response import Response
from .permissions import IsOwner


class BusinessProfileView(generics.RetrieveUpdateAPIView):
    queryset = BusinessProfile.objects.select_related('user').all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__id'


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.select_related('user').all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__id'



# Für ALLE Profile (ohne ID):
class BusinessProfileListView(generics.ListAPIView):
    queryset = BusinessProfile.objects.select_related('user').all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerProfileListView(generics.ListAPIView):
    queryset = CustomerProfile.objects.select_related('user').all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]    
    

class UserProfileDetailView(APIView):
       permission_classes = [permissions.IsAuthenticated,IsOwner]

       def _load_profile(self, request, pk):    
         profile = get_object_or_404(Profile, user__id=pk)
         self.check_object_permissions(request, profile)
         return profile 

       def get(self, request, pk):
         profile = self._load_profile(request, pk)
         if profile.user_type == 'business':
            business_profile = get_object_or_404(BusinessProfile, user__id=pk)
            serializer = BusinessProfileSerializer(business_profile)
         else:
            customer_profile = get_object_or_404(CustomerProfile, user__id=pk)
            serializer = CustomerProfileSerializer(customer_profile)
         return Response(serializer.data)     


       def patch(self,request,pk):
           profile = self._load_profile(request, pk)
           if profile.user_type == 'business':
               instance=get_object_or_404(BusinessProfile,user__id=pk)
               serializer=BusinessProfileSerializer(instance,data=request.data, partial=True)
           else:
               instance=get_object_or_404(CustomerProfile,user__id=pk)  
               serializer=CustomerProfileSerializer(instance,data=request.data,partial=True)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=200)
           return Response(serializer.errors, status=400)        