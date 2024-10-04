tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_file_content",
            "description": "Fetches the contents of the provided file paths.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "A list of file paths to fetch content from"
                    }
                },
                "required": ["file_paths"],
                "additionalProperties": False,
            }
        }
    },
]

