from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from .serializers import UserMeSerializer, AbonneRegisterSerializer

User = get_user_model()


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = attrs.copy()
        login = attrs.get("username")
        if login and "@" in login:
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


class AbonneRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AbonneRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "detail": "Compte abonné(e) créé avec succès.",
                "user": UserMeSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )
