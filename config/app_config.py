# application
app_description = 'Cli Application gets all the repos from Github based on username passed. These repos can be filtered based on repo_name or created_after. If repo_name and created_after both args are passed then prefrence is given to repo_name.'
example_user = 'GarimaDamani'
example_repo = 'python_learnings'
example_created = '2019-08-06'
decode = 'utf-8'
data_from_cache_msg = 'Found your data in cache'
data_from_github_msg = 'Not found in cache. Getting from Github'
data_not_found = 'Sorry! requested data is not matched with any repo or created time'

# redis
host = 'localhost'
port = 6379
db = 0
timeout = 20
success_conn_msg = 'Connection to redis is OK'
failure_conn_msg = 'Unable to make connection to redis. Exiting'

# Github
github_url = 'https://api.github.com/'

# args
user_arg = '--username'
repo_arg = '--repo_name'
created_arg = '--created_after'
