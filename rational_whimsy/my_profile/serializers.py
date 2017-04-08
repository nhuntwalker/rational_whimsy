"""A serializer for the JSON data returned from GitHub."""
from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    """A serializer for an individual repo."""

    name = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=1024)
    repo_url = serializers.URLField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    stargazers_count = serializers.IntegerField()
    watchers_count = serializers.IntegerField()
    forks = serializers.IntegerField()
    open_issues = serializers.IntegerField()
    language = serializers.CharField(max_length=256)
