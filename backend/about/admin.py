from django.contrib import admin
from .models import (
    AboutInfo, TimelineEvent, Founder, StaffMember,
    Value, KeyStat, Vision, ExamResult
)

@admin.register(AboutInfo)
class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "founded_date")


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "order")
    ordering = ("order",)


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(KeyStat)
class KeyStatAdmin(admin.ModelAdmin):
    list_display = ("label", "value")


@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ("exam_name", "success_rate", "total_students")
