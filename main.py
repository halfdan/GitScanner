import os
from github import Github
import git
import click
import config
import csv

hub = Github(config.GITHUB_ACCESS_TOKEN)

if config.SEARCH_ORGANISATION:
    gh_repos = list(hub.get_organization(config.SEARCH_ORGANISATION).get_repos())
else:
    gh_repos = list(hub.get_user().get_repos())

local_repos: git.Repo = []
with click.progressbar(gh_repos, label="Cloning/Updating Repositories", length=len(gh_repos)) as remote_repos:
    for gh_repo in remote_repos:
        clone_url = gh_repo.clone_url

        path = os.getcwd() + "/repos/" + gh_repo.full_name

        try:
            local_repos.append(git.Repo(path))
            g = git.Git(path)
            g.pull("origin")
        except git.exc.NoSuchPathError:
            local_repo = git.Repo.clone_from(gh_repo.clone_url, path)
            local_repos.append(local_repo)

commits: git.Commit = []
with click.progressbar(local_repos, label="Extracting commits", length=len(local_repos)) as local_repos:
    for repo in local_repos:
        for commit in repo.iter_commits(all=True, no_merges=True, reverse=True):
            if commit.author.email in config.SEARCH_COMMIT_AUTHORS:
                commits.append(commit)


# Sort commits by authored_date
sorted_commits = sorted(commits, key=lambda c: c.authored_date)
file = open("commits.csv", "w")
writer = csv.writer(file)

with click.progressbar(sorted_commits, label="Exporting commits", length=len(sorted_commits)) as commits:
    writer.writerow(["repository", "author", "authored_date", "authored_tz_offset", "message"])
    for commit in commits:
        repo_url = list(commit.repo.remotes.origin.urls)[0]
        writer.writerow([repo_url, commit.author.email, commit.authored_date, commit.author_tz_offset, commit.message.strip()])

    
file.close()