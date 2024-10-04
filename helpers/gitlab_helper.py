import gitlab
import json

from configs import config

gl = gitlab.Gitlab(
    url=config.gitlab_url, 
    private_token=config.gitlab_pat
)

def get_project_issue_details(project_path, issue_iid) -> dict:
    project = gl.projects.get(project_path)
    issue = project.issues.get(issue_iid)

    return {
        "project_id": project.id,
        "repo_default_branch": project.default_branch,
        "repo_url": project.http_url_to_repo,
        "issue_title": issue.title,
        "issue_id": issue.id,
        "issue_iid": issue.iid,
        "issue_description": issue.description,
        "issue_state": issue.state,
        "issue_assignee": issue.assignees[0].get('username')
    }

def post_comments_to_issue(project_id, issue_iid, comment_text):
    project = gl.projects.get(project_id)
    issue = project.issues.get(issue_iid)
    issue.notes.create({'body': comment_text})

    
