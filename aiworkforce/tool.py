import requests
from aiworkforce.utils import save_all_objects
from aiworkforce.types import FilterType

def get_tool(tool_id:str, region_id:str, project_id:str, api_key:str, limit:int=1):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/list"
    response = requests.get(
        path, 
        headers=headers, 
        params={
            "page_size": limit, 
            "filters": f'[{{"field":"project","condition":"==","condition_value":"{project_id}","filter_type":{FilterType.EXACT_MATCH}}},{{"field":"studio_id","condition":"==","condition_value":"{tool_id}","filter_type":{FilterType.EXACT_MATCH}}}]'
        }
    )
    return response.json()['results'][0]


def get_all_tools(region_id:str, project_id:str, api_key:str, limit:int=50000):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/list"
    response = requests.get(
        path, 
        headers=headers, 
        params={
            "page_size" : limit,
            "filters" : f'[{{"field":"project","condition":"==","condition_value":"{project_id}","filter_type":{FilterType.EXACT_MATCH}}}]'
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


def get_tool_run_history(tool_id:str, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/run_history/list"
    payload = {
        "page_size": 999999999999,
        "filters": f'[{{"filter_type":{FilterType.EXACT_MATCH},"field":"project","condition":"==","condition_value":"{project_id}"}},{{"filter_type":{FilterType.EXACT_MATCH},"field":"studio_id","condition":"==","condition_value":"{tool_id}"}}]',
        "with_agent_details": True
    }
    response = requests.get(path, headers=headers, params=payload)
    return response.json()


def trigger_tool(tool_id:str, region_id:str, project_id:str, api_key:str, tool_inputs:dict):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/{tool_id}/trigger_async" #
    payload = {
        "executor": {"type": "run_chain"},
        "max_job_duration": "minutes",
        "params": tool_inputs,
        "studio_id": tool_id,
    }
    response = requests.post(path, headers=headers, json=payload)
    return response.json()


def delete_tools(tool_ids:list, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/bulk_delete"
    response = requests.post(path, json={"ids": tool_ids}, headers=headers)
    return response.json()


def update_tool(tool_json:dict, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/studios/bulk_update"
    payload = {
        "updates": [tool_json],
        "partial_update": True,
        "insert_if_not_exists": False
    }
    response = requests.post(path, json=payload, headers=headers)
    return response.json()


def save_tools_to_file(tools, folderpath):
    save_all_objects(tools, folderpath, "tools")
