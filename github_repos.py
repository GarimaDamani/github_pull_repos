import sys
import json
import time
import redis
import requests
import argparse
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
from config import app_config


class Redis:
    pool = None

    def __init__(self):
        self.pool = redis.ConnectionPool(host=app_config.host, port=app_config.port, db=app_config.db)

    def make_connection(self):
        return redis.Redis(connection_pool=self.pool)

    def check_connection(self):
        redis_server = self.make_connection()
        return redis_server.ping()

    def set_data(self, username, user_repos):
        redis_server = self.make_connection()
        time_after_twenty_min = datetime.now() + timedelta(minutes=app_config.timeout)
        json_user_repos = json.dumps(user_repos)
        redis_server.set(username, json_user_repos)
        redis_server.expireat(username, time_after_twenty_min)

    def get_data(self, username):
        redis_server = self.make_connection()
        if redis_server.exists(username):
            unpack_user_repos = json.loads(redis_server.get(username).decode(app_config.decode))
            return unpack_user_repos
        return False


class Github(object):
    github_url = None
    redis_obj = None

    def __init__(self, redis_class):
        self.github_url = app_config.github_url
        self.redis_obj = redis_class()
        if self.redis_obj.check_connection():
            print(app_config.success_conn_msg)
        else:
            sys.exit(app_config.failure_conn_msg)

    def get_user_repo(self, username, repo_name, created_after):
        try:
            user_repos = self._get_data_from_cache(username)
            if bool(user_repos):
                print(app_config.data_from_cache_msg)
                self._print_repo_data(user_repos, repo_name, created_after)
            else:
                print(app_config.data_from_github_msg)
                self._set_data_in_cache(username)
                user_repos = self._get_data_from_cache(username)
                self._print_repo_data(user_repos, repo_name, created_after)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def _set_data_in_cache(self, username):
        user_repos = self._query_github(username)
        self.redis_obj.set_data(username, user_repos)

    def _get_data_from_cache(self, username):
        return self.redis_obj.get_data(username)

    def _query_github(self, username):
        url = 'users/' + username + '/repos'
        github_repos = requests.get(self.github_url + url)
        if github_repos.status_code == 200:
            parsed_data = json.loads(github_repos.content)
            user_repos = []
            for repo_data in parsed_data:
                temp = {}
                temp['html_url'] = str(repo_data['html_url'])
                temp['forks_count'] = int(repo_data['forks_count'])
                temp['created_at'] = str(repo_data['created_at'])
                user_repos.append(temp)
            return user_repos
        else:
            return False

    @staticmethod
    def _print_repo_data(user_repos, repo_name, created_after):
        found_element = False
        if repo_name is not None:
            for item in user_repos:
                if repo_name in item['html_url']:
                    print('html_url : ', item['html_url'])
                    print('forks_count : ', item['forks_count'])
                    print('created_at : ', item['created_at'])
                    found_element = True
        elif created_after is not None:
            created_after = datetime.strptime(created_after, '%Y-%m-%d')
            for item in user_repos:
                date = datetime.strptime(item['created_at'].split('T')[0], '%Y-%m-%d')
                if date > created_after:
                    for key, value in item.items():
                        print(key, ' : ', value)
                        found_element = True
        else:
            for item in user_repos:
                for key, value in item.items():
                    print(key, ' : ', value)
                    found_element = True
        if found_element is not True:
            print(app_config.data_not_found)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=app_config.app_description)
    parser.add_argument(app_config.user_arg, required=True, help=app_config.example_user)
    parser.add_argument(app_config.repo_arg, help=app_config.example_repo)
    parser.add_argument(app_config.created_arg, help=app_config.example_created)

    args = parser.parse_args()

    github = Github(Redis)
    github.get_user_repo(args.username, args.repo_name, args.created_after)
    time.sleep(600)  # Sleep for 10 minutes
    github.get_user_repo(args.username, args.repo_name, args.created_after)
    time.sleep(1260)  # Sleep for 21 minutes
    github.get_user_repo(args.username, args.repo_name, args.created_after)
