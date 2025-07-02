from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializer import RegistrationSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user_auth_app.models import Profile
from profile_app.models import CustomerProfile,BusinessProfile


GUEST_LOGINS = {
    'customer': {'username': 'andrey', 'password': 'asdasd'},
    'business': {'username': 'kevin', 'password': 'asdasd24'}
}


class RegistrationView(generics.CreateAPIView):
    serializer_class=RegistrationSerializer
    permission_classes = [AllowAny]



    def create(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        data={}
        if serializer.is_valid():
            user=serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data={
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "type": user.profile.user_type
            }
            return Response(data,status=HTTP_201_CREATED)
        
        else:
           response_data = {
            "errors": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_type = None
        for u_type, creds in GUEST_LOGINS.items():
            if creds['username'] == username and creds['password'] == password:
                user_type = u_type
                break

        if user_type:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@guest.com'}
            )
            if created:
                user.set_password(password)
                user.save()

            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={'user_type': user_type}
            )

            if user_type == 'business':
                BusinessProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'user_type': 'business',
                        'username': user.username,
                        'email': user.email,
                        'first_name': '',
                        'last_name': '',
                        'tel': '',
                        'location': '',
                        'description': '',
                        'working_hours': '',
                        'file': None
                    }
                )
            else:  # customer
                CustomerProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'user_type': 'customer',
                        'username': user.username,
                        'email': user.email,
                        'first_name': '',
                        'last_name': '',
                        'file': None
                    }
                )

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "type": user_type
            }, status=HTTP_200_OK)

        # Normale Authentifizierung (kein Gast)
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "type": user.profile.user_type
            }, status=HTTP_200_OK)

        return Response({"error": "Ungültiger Benutzername oder Passwort"},
                        status=HTTP_401_UNAUTHORIZED)





