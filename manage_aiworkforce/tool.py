import requests
from manage_aiworkforce.utils import save_all_objects


def get_all_tools(region_id:str, project_id:str, api_key:str, limit:int=5000):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/list"
    response = requests.get(
        path, 
        headers=headers, 
        params={
            "page_size" : limit,
            "filters" : f'[{{"field":"project","condition":"==","condition_value":"{project_id}","filter_type":"exact_match"}}]'
        }
    )
    return response.json()['results']


def create_tools(tool_jsons:list, region_id:str, project_id:str, api_key:str, partial_update:bool=True, insert_if_not_exists:bool=True):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/bulk_update"
    payload = {
        "updates": tool_jsons,
        "partial_update": partial_update,
        "insert_if_not_exists": insert_if_not_exists
    }
    response = requests.post(path, json=payload, headers=headers)
    
    return response.json()


def delete_tools(tool_ids:list, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/bulk_delete"
    response = requests.post(path, json={"ids": tool_ids}, headers=headers)
    return response.json()

def save_tools_to_file(tools, folderpath):
    save_all_objects(tools, folderpath, "tools")
