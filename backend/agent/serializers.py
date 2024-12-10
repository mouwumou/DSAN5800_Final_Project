from rest_framework import serializers

from .models import Tool

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ('id', 'name', 'description', 'prompt_template', 'created_at', 'updated_at')