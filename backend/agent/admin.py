from django.contrib import admin

from .models import History
# Register your models here.

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'created_at')
    search_fields = ('user__username', 'session_id')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
