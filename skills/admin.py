from django.contrib import admin
from .models import Skill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'location', 'availability', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_filter = ('availability', 'created_at')
