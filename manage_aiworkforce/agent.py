import requests
from typing import Optional

from manage_aiworkforce.utils import save_all_objects
from manage_aiworkforce.types import FilterType


def get_all_agents(region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/list"
    response = requests.post(
        path, 
        headers=headers, 
        params={
            "page_size" : 50000, 
            "filters" : [{"field":"project","condition":"==","condition_value":project_id,"filter_type":FilterType.EXACT_MATCH}]
        }
    )
    
    return response.json()['results']


def get_agent_tools(agent_id:str, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/tools/list"
    body = {"agent_ids": [agent_id]}
    response = requests.post(path, body=body, headers=headers)
    
    return response.json().get("results", [])


def create_agent(agent_json:dict, region_id:str, project_id:str, api_key:str, partial_update: Optional[bool] = False):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/upsert"
    body = {
        **agent_json,
        "partial_update": partial_update,
    }
    response = requests.post(path, json=body, headers=headers)
    return response.json()


def save_agents_to_file(agents:list, folderpath:str):
    save_all_objects(agents, folderpath, "agents")
