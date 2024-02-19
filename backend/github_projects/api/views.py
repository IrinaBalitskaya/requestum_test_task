from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from github_projects.api.serializers import CommonContributorsSerializer

from drf_yasg.utils import swagger_auto_schema

from github_projects.api.serializers import CommonContributorsInputSerializer

from github_projects.services import GithubRepos


class GithubViewSet(GenericViewSet):

    @swagger_auto_schema(query_serializer=CommonContributorsInputSerializer)
    @action(detail=False,
            serializer_class=CommonContributorsSerializer,
            url_name='get-common-contributors-repos',
            url_path='get-common-contributors-repos')
    def get_common_contributors_repos(self, request, *args, **kwargs):
        github_repo_data = CommonContributorsInputSerializer(data=request.query_params)
        github_repo_data.is_valid(raise_exception=True)
        github_repo_url = github_repo_data.data['github_repo_url']

        try:
            github_repos = GithubRepos()
            serialized_response = []
            common_contributors = github_repos.get_common_contributors(github_repo_url)
            for key, value in common_contributors.items():
                repo_object = {'name': key, 'url': f'https://github.com{key}', 'common_contributors_count': value}
                serialized_response.append(repo_object)
            result = self.get_serializer(serialized_response, many=True)
            return Response(result.data)
        except APIException as e:
            return Response(data={"github_repo_url": [str(e)]}, status=400)
