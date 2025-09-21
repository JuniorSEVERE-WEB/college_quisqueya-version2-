from rest_framework import serializers
from .models import ReportSession, SubjectCoefficient, Grade

class ReportSessionSerializer(serializers.ModelSerializer):
    trimester_display = serializers.CharField(source="get_trimester_display", read_only=True)
    step_display = serializers.CharField(source="get_step_display", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReportSession
        fields = [
            "id", "title", "classroom", "academic_year",
            "trimester", "trimester_display",
            "step", "step_display",
            "is_active", "created_at", "created_by",
        ]
        read_only_fields = ["created_at", "created_by"]

class SubjectCoefficientSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCoefficient
        fields = ["id", "classroom", "subject", "academic_year", "coefficient"]

class GradeSerializer(serializers.ModelSerializer):
    # Champs « nom » en lecture seule (optionnels, utiles dans la liste)
    program_name = serializers.CharField(source="program.name", read_only=True)
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    student_name = serializers.CharField(source="student.full_name", read_only=True)

    class Meta:
        model = Grade
        fields = [
            "id", "program", "program_name",
            "classroom", "classroom_name",
            "student", "student_name",
            "subject", "subject_name",
            "report_session",
            "note",
        ]

    def validate(self, attrs):
        # Vérifications de cohérence basiques (protégées si champs manquent)
        classroom = attrs.get("classroom") or getattr(self.instance, "classroom", None)
        program = attrs.get("program") or getattr(self.instance, "program", None)
        student = attrs.get("student") or getattr(self.instance, "student", None)
        subject = attrs.get("subject") or getattr(self.instance, "subject", None)
        report_session = attrs.get("report_session") or getattr(self.instance, "report_session", None)

        # program vs classroom.program (si attribut disponible)
        if program and classroom and hasattr(classroom, "program") and classroom.program_id and program.id != classroom.program_id:
            raise serializers.ValidationError("Program must match classroom.program.")

        # student.classroom vs classroom (si attribut disponible)
        if student and classroom and hasattr(student, "classroom_id") and student.classroom_id and student.classroom_id != getattr(classroom, "id", None):
            raise serializers.ValidationError("Student must belong to the selected classroom.")

        # report_session.classroom vs classroom
        if report_session and classroom and getattr(report_session, "classroom_id", None) != getattr(classroom, "id", None):
            raise serializers.ValidationError("Report session must belong to the same classroom.")

        return attrs