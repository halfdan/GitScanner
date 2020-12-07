"""
1. Go to: https://github.com/settings/tokens/new
2. Enable all repo.* scopes, admin:org/read:org scope
"""
GITHUB_ACCESS_TOKEN = "TOKEN"

"""
This specifies the organisation we want to search. 

If left blank all repos the user has access to will be checked out.
"""
SEARCH_ORGANISATION = "ORG"

"""
List of commit authors to search for
"""
SEARCH_COMMIT_AUTHORS = ["EMAIL1", "EMAIL2"]