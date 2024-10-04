import re

def parse_payload(payload):
    try:
        res = {
            "project_path": None,
            "issue_id": None
        }
        
        # Extract the first section
        section = payload.get("sections", [])[0]

        # Extract the project path from activitySubtitle
        activity_subtitle = section.get("activitySubtitle", "")
        project_path_match = re.search(r'in \[(.*?)\]', activity_subtitle)
        if project_path_match:
            res["project_path"] = project_path_match.group(1).replace(' ', '')
        
        # Extract the issue ID from activityText
        activity_text = section.get("activityText", "")
        issue_id_match = re.search(r'#(\d+)', activity_text)
        if issue_id_match:
            res["issue_id"] = issue_id_match.group(1)

        return res
    
    
    except Exception as e:
        print(e)