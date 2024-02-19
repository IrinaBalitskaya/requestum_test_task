import logging

from django.conf import settings
from github import Github, Auth, GithubException
import requests
from requests.adapters import HTTPAdapter, Retry
from rest_framework.exceptions import APIException

logging.basicConfig(level=logging.INFO)


class GithubRepos:

    def __init__(self):
        # Init GitHub REST API / GraphQL headers
        print(settings.GITHUB_API_KEY)
        github_auth = Auth.Token(settings.GITHUB_API_KEY)
        self.github_api = Github(auth=github_auth)
        self.headers = {"Authorization": f"Bearer {settings.GITHUB_API_KEY}"}

    def get_common_contributors(self, url: str) -> dict:
        """Gets similar repos and number of common contributors for provided repo URL.

        :param url: str - GitHub repo URL.
        :return: dict: key - repo_name, value - contributors count.
        :raises: APIException if incorrect GitHub repo URL was provided.
        """
        _, owner, repo_name = url.rstrip('/').split('/')[-3:]

        try:
            # Fetching repo details
            repo = self.github_api.get_repo(f"{owner}/{repo_name}")
        except GithubException as e:
            print(e)
            raise APIException("URL does not match any Github Repos")

        # Getting repo contributors
        repo_contributors = repo.get_contributors()
        # Getting contributors' node ids
        contributors_node_id_list = [contributor_node_id.node_id for contributor_node_id in repo_contributors]
        # Splitting contributors_node_id_list to chunks of size 10 and less to request details from GitHub API
        contributors_node_id_sublists = [contributors_node_id_list[i:i + 10] for i in
                                         range(0, len(contributors_node_id_list), 10)]

        repos_dict = {}
        list_repos_contributed_to = []
        # Getting info about repos to which users contributed to lately
        for sublist in contributors_node_id_sublists:
            result = self.get_contributors_repos(sublist)
            if result and 'data' in result:
                data = result['data']['nodes']
                list_repos_contributed_to.extend(data)

        # Creating dict from fetched data where key - repo name, value - number of contributors
        for repo in list_repos_contributed_to:
            if repo:
                for rp in repo['repositoriesContributedTo']['nodes']:
                    if rp['resourcePath'] not in repos_dict:
                        repos_dict[rp['resourcePath']] = 1
                    else:
                        repos_dict[rp['resourcePath']] += 1
        # Sorting dict by biggest value
        repos_dict = {k: v for k, v in sorted(repos_dict.items(), reverse=True, key=lambda item: item[1])}

        # Removing provided repo name if it is in dict
        if f'/{owner}/{repo_name}' in repos_dict:
            del repos_dict[f'/{owner}/{repo_name}']

        # Returning first 5 repos
        return dict(list(repos_dict.items())[:5])

    def get_contributors_repos(self, sublist: list) -> dict | None:
        """Gets contributors' repos data from GitHub GraphQL
    
        :param sublist: List of contributors' node id
        :return: JSON data about repos or None if GitHub server returned error and retrying failed
        """

        retry_number = 3
        query = """
                    query {
                      nodes(ids: """ f'{str(sublist).replace('\'', '\"')}' """) {
                        ... on User {
                          repositoriesContributedTo(last: 50) {
                            nodes {
                              resourcePath
                            }
                          }
                        }
                      }
                    }
                """
        session = requests.Session()
        retries = Retry(total=retry_number, status_forcelist=[502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        for _ in range(retry_number):
            request = session.post('https://api.github.com/graphql', json={'query': query},
                                   headers=self.headers)
            if request.status_code == 200:
                return request.json()
            else:
                logging.info(msg="Retrying")
        return None
