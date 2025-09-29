from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    AboutInfo, TimelineEvent, Founder, StaffMember,
    Value, KeyStat, Vision, ExamResult
)
from rest_framework.permissions import AllowAny
from .serializers import (
    AboutInfoSerializer, TimelineEventSerializer, FounderSerializer, StaffMemberSerializer,
    ValueSerializer, KeyStatSerializer, VisionSerializer, ExamResultSerializer
)

class AboutPageView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = {
            "about_info": AboutInfoSerializer(AboutInfo.objects.first()).data if AboutInfo.objects.exists() else None,
            "timeline": TimelineEventSerializer(TimelineEvent.objects.all(), many=True).data,
            "founders": FounderSerializer(Founder.objects.all(), many=True).data,
            "staff": StaffMemberSerializer(StaffMember.objects.all(), many=True).data,
            "values": ValueSerializer(Value.objects.all(), many=True).data,
            "keystats": KeyStatSerializer(KeyStat.objects.all(), many=True).data,
            "vision": VisionSerializer(Vision.objects.all(), many=True).data,
            "exam_results": ExamResultSerializer(ExamResult.objects.all(), many=True).data,
        }
        return Response(data)
