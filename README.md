# Github Pull Repos

Create a cli application which will
* Get information of all repos from GitHub based on username
* Save it in redis with an expiry for 20 minutes
* Next time when same username is called, serve the repo's details from redis
* If repos/data is expired then serve from Github 
* Create objects of the repositories that you get from GitHub
* Provide a search functionality with repo_name, created_after, fork_count
* If user provides both the args repo_name and created_after then give priority to repo_name arg

Below is the commands that if should support. 

`python app.py —username='username' —repo_name='repo_name_optional' —created_after='created_after_optional'`

# Requirements
* Python 3.6
* pip3

# Set up details
* `git clone git@github.com:GarimaDamani/github_pull_repos.git`
* Install redis locally using [link](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)
* Create a virtualenv inside `pull_github_repos` directory. Installation steps [here](https://medium.com/@garimajdamani/https-medium-com-garimajdamani-installing-virtualenv-on-ubuntu-16-04-108c366e4430)
* Execute the below steps

```
cd pull_github_repos
pip3 install -r requirements.txt
python3 github_repos.py --help
python3 github_repos.py --username 'GarimaDamani'
python3 github_repos.py --username 'GarimaDamani' --repo_name='shell_learning' --created_after='2019-08-19'
python3 github_repos.py --username 'GarimaDamani' --created_after='2019-08-25'
```
