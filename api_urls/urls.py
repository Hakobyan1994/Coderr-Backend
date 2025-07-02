from django.urls import path
from user_auth_app.api.views import RegistrationView,LoginView
from profile_app.api.views import UserProfileDetailView,BusinessProfileView,CustomerProfileView,BusinessProfileListView,CustomerProfileListView
from reviews_app.api.views import ReviewListCreateView,ReviewDetailView
from offers_app.api.views import OfferListCreateView,OfferRetrieveUpdateDestroyView,OfferDetailView
from orders_app.api.views import ListCreateOrderView,SingleOrderView,OrderCountView,CompletedOrderCountView
from base_info_app.api.views import BaseInfoView



urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
    path('login/',LoginView.as_view(),name="login"),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/<int:user__id>',BusinessProfileView.as_view(),name='profile-business'),
    path('profiles/customer/<int:user__id>',CustomerProfileView.as_view(),name='profile-customer'),
    path('profiles/business/',BusinessProfileListView.as_view(),name='profile-business'),
    path('profiles/customer/',CustomerProfileListView.as_view(),name='profile-customer'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-detail-single'),
    path('orders/', ListCreateOrderView.as_view(), name='list-orders'),
    path('orders/<int:pk>/', SingleOrderView.as_view(), name='single-order'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-count'),
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]
