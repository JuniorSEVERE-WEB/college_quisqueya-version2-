import uuid
from rest_framework import viewsets, generics, permissions, serializers, status
from rest_framework.response import Response
from academics.models import AcademicYear
from programs.models import Classroom
from accounts.models import User
from .models import Student
from .serializers import StudentSerializer


# ---------------------------
# ViewSet privé (protégé JWT)
# ---------------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ["academic_year", "user", "id"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["id", "user__username"]

    def get_queryset(self):
        active = AcademicYear.objects.filter(is_active=True).first()
        if active:
            return (
                Student.objects
                .filter(academic_year=active)
                .select_related("user", "academic_year")
            )
        return Student.objects.none()


# ---------------------------
class StudentRegisterSerializer(serializers.Serializer):
    # Champs User
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # Champs Student
    date_of_birth = serializers.DateField()
    parent_phone = serializers.CharField()
    student_phone = serializers.CharField(required=False, allow_blank=True)
    parent_email = serializers.EmailField(required=False, allow_blank=True)
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    birth_certificate = serializers.FileField(required=False, allow_null=True)
    last_school_report = serializers.FileField(required=False, allow_null=True)

    # --- Validations personnalisées ---
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d’utilisateur est déjà pris.")
        return value

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        # 1. Créer le User
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role="student",
        )

        # 2. Associer à l’année académique active
        academic_year = AcademicYear.objects.filter(is_active=True).first()
        if not academic_year:
            raise serializers.ValidationError("Aucune année académique active trouvée.")

        # 3. Générer un matricule unique
        matricule = f"{academic_year.name}-{uuid.uuid4().hex[:6].upper()}"

        # 4. Créer le Student
        student = Student.objects.create(
            user=user,
            academic_year=academic_year,
            classroom=validated_data["classroom"],
            date_of_birth=validated_data["date_of_birth"],
            parent_phone=validated_data["parent_phone"],
            student_phone=validated_data.get("student_phone", ""),
            parent_email=validated_data.get("parent_email", ""),
            birth_certificate=validated_data.get("birth_certificate"),
            last_school_report=validated_data.get("last_school_report"),
            matricule=matricule,
        )
        return student

# ---------------------------
# Vue publique inscription
# ---------------------------
class StudentRegisterView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()

        # Réponse avec StudentSerializer pour inclure infos liées
        output_serializer = StudentSerializer(student)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

