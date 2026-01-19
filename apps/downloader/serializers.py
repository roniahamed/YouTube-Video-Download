from rest_framework import serializers

class AnalyzeSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

class DownloadSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    format_id = serializers.CharField(required=True)
