import os
import git

from configs import config

def clone_private_repo(repo_url, local_dir = None, branch="main"):
    if not local_dir:
        local_dir = config.default_tmp_dir

    repo_url = repo_url.replace(
        "https://", 
        f"https://{config.gitlab_bot_uname}:{config.gitlab_pat}@"
    )
    
    tmp_dir_name = repo_url.split('/')[-1].split('.')[0]
    destination_dir = os.path.join(local_dir, tmp_dir_name)
    git.Repo.clone_from(repo_url, destination_dir, branch=branch)

    return destination_dir

