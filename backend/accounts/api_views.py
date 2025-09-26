from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserMeSerializer

class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = attrs.copy()
        login = attrs.get("username")
        if login and "@" in login:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=login)
                data["username"] = getattr(user, User.USERNAME_FIELD)
            except User.DoesNotExist:
                pass
        return super().validate(data)

class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserMeSerializer(request.user).data)