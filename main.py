from fastapi import FastAPI, Request
import uvicorn

from helpers.payload_parser import parse_payload
from helpers.gitlab_helper import get_project_issue_details, post_comments_to_issue
from helpers.git_helper import clone_private_repo
from llm.openai import generate_response

app = FastAPI()

@app.post("/webhook")
async def gitlab_webhook(request: Request):

    try:
        payload = await request.json()
        payload = parse_payload(payload)
        
        # get issue details 
        issue_details = get_project_issue_details(
            payload.get('project_path'),
            payload.get('issue_id')
        )

        # clone repo
        repo_path = clone_private_repo(
            issue_details.get('url')
        )

        # generate response
        messages = generate_response(repo_path, issue_details)

        # post comment to issue
        post_comments_to_issue(
            project_id=issue_details.get('id'),
            issue_iid=issue_details.get('iid'),
            comment_text=messages[-1].get('content')
        )

    except:
        print("fail to parse payload")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")