import openai
import json

from helpers import repomap, functions
from configs import config
from .tools import tools
from .prompts import system_prompt

openai.api_key = config.openai_api_key

# TODO: 1. take in parameter
# TODO: 2. make function call loopable with max try 
# TODO: 3. abstract generic functions like calling for response 
# TODO: 4. make function calling dynamic by maintaining a callable function map

def generate_response(repo_dir: str, issue):
    repo_map = repomap.analyze_repository(repo_dir)
    issue_title = issue.get('issue_title')
    issue_description = issue.get('issue_description')
    
    messages = [{
        "role": "system",
        "content": system_prompt.format(
            repo_map=repo_map, 
            issue_title=issue_title,
            issue_description=issue_description)
    }]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )

    if not response.choices[0].message.tool_calls:
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        return messages
    
    tool_call = response.choices[0].message.tool_calls[0]
    tool_args = json.loads(tool_call.function.arguments)
    
    if tool_call.function.name == "fetch_file_content":
        file_paths = tool_args.get("file_paths")
        file_content = functions.fetch_file_content(file_paths)

        # supposedly we don't need to reconstruct this ourself 
        # in the docs seems like we can just append response.choices[0].message
        # but it won't work at this version so yeah.. 
        messages.append({
            "role": "assistant",
            "tool_calls": [{
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            }]
        })
        
        messages.append({
            "role":"tool", 
            "tool_call_id": tool_call.id , 
            "name": tool_call.function.name, 
            "content": file_content
        })
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

    return messages
    
    
    

    















