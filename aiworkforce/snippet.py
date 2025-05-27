import requests

def upsert_snippet(region_id: str, project_id: str, api_key: str, snippet_name: str, snippet_content: str, title:str = None, description:str = None):
    """Upserts a snippet to the Relevance platform."""
    headers = {"Content-Type": "application/json", "Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    url = f"{base_url}/projects/snippets/list"

    response = requests.get(url, headers=headers)
    current_snippets = response.json()

    url = f"{base_url}/projects/snippets/upsert"

    payload = {"name": snippet_name.lower(), "content": snippet_content}

    for current in current_snippets:
        if current.get('name', '').lower() == snippet_name.lower():
            payload['_id'] = current.get('_id')
            payload['title'] = current.get('title', snippet_name)
            payload['description'] = current.get('description', '')
            payload['order'] = current.get('order', 1)

    if title:
        payload['title'] = title
    if description:
        payload['description'] = description
    if 'order' not in payload:
        payload['order'] = 1

    response = requests.post(url, json=payload, headers=headers)

    return response.json()

def append_to_existing_snippet(region_id: str, project_id: str, api_key: str, snippet_name: str, snippet_content: str):
    """Appends to an existing snippet on the Relevance platform."""
    headers = {"Content-Type": "application/json", "Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    url = f"{base_url}/projects/snippets/list"

    response = requests.get(url, headers=headers)
    current_snippets = response.json()

    url = f"{base_url}/projects/snippets/upsert"

    payload = None

    for current in current_snippets:
        if current.get('name', '').lower() == snippet_name.lower():
            payload = {"name": snippet_name.lower()}
            payload['_id'] = current.get('_id')
            payload['title'] = current.get('title', snippet_name)
            payload['description'] = current.get('description', '')
            payload['order'] = current.get('order', 1)
            payload['content'] = current.get('content', '') + '\n' + snippet_content

    if not payload:
        raise Exception(f"Snippet {snippet_name} not found. Please create a new snippet first in order to append new content to it.")
    
    response = requests.post(url, json=payload, headers=headers)

    return response.json()