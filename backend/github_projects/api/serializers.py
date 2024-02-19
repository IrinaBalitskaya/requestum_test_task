from rest_framework import serializers


class CommonContributorsSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()
    common_contributors_count = serializers.IntegerField()


class CommonContributorsInputSerializer(serializers.Serializer):
    github_repo_url = serializers.URLField()

    def validate_github_repo_url(self, value):
        """
             Check url is a Github url.
             """
        if 'github.com' not in value:
            raise serializers.ValidationError("Not a Github URL")
        return value
