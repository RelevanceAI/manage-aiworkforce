import requests


def get_all_knowledge(region_id, project_id, api_key):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/sets/list"
    body = {
        "filters": [],
        "sort": [{"update_date":"desc"}]
    }
    response = requests.post(path, body=body, headers=headers)

    return response.json().get("results", [])


def get_knowledge(region_id:str, project_id:str, api_key:str, knowledge_set: str, max_results: int = 5000):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/list"
    body = {
        "knowledge_set": knowledge_set,
        "page_size": max_results,
        "sort": [{"insert_date_": "desc"}]
    }
    response = requests.post(path, body=body, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    return {"error": response.text}


def delete_knowledge(region_id:str, project_id:str, api_key:str, knowledge_set: str) -> bool:
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/sets/delete"
    body = {"knowledge_set": knowledge_set}
    response = requests.post(path, body=body, headers=headers)

    return response.status_code == 200


def create_knowledge(region_id:str, project_id:str, api_key:str, knowledge_set: str) -> bool:
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/add"
    body = {"knowledge_set": knowledge_set}
    response = requests.post(path, body=body, headers=headers)

    return response.status_code == 200


def get_knowledge_metadata(region_id:str, project_id:str, api_key:str, knowledge_set: str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/sets/{knowledge_set}/get_metadata"
    response = requests.get(path, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
