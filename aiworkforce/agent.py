import requests
import json
from typing import Optional

from aiworkforce.utils import save_all_objects
from aiworkforce.types import FilterType


def get_all_agents(region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/list"
    response = requests.post(
        path, 
        headers=headers, 
        params=json.dumps({
            "page_size" : 50000, 
            "filters" : [{"field":"project","condition":"==","condition_value":project_id,"filter_type":FilterType.EXACT_MATCH}]
        })
    )
    
    return response.json()['results']


def get_agents_tool_metadata(agent_id:str, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/tools/list"
    body = {"agent_ids": [agent_id]}
    response = requests.post(path, json=body, headers=headers)
    
    return response.json().get("results", [])


def get_agent_tools(agent_id:str, region_id:str, project_id:str, api_key:str):
    headers = {"Content-Type": "application/json", "Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/{agent_id}/tools/list"
    response = requests.post(path, headers=headers)
    
    return response.json().get("chains", [])


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


def delete_agent(agent_id:str, region_id:str, project_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/{agent_id}/delete"
    response = requests.post(path, json={}, headers=headers)
    
    return response.json()

def save_agents_to_file(agents:list, folderpath:str):
    save_all_objects(agents, folderpath, "agents")


def update_agent(agent_id:str, region_id:str, project_id:str, api_key:str, agent_json:dict):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/upsert"
    agent_json["agent_id"] = agent_id
    response = requests.post(path, json=agent_json, headers=headers)
    return response.json()


def schedule_message_to_agent(region_id: str, project_id: str, agent_id: str, message: str, conversation_id: str, minutes_until_schedule: int, api_key: str) -> dict:
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/{agent_id}/scheduled_triggers_item/create"
    payload = {
        "message": message,
        "conversation_id": conversation_id,
        "minutes_until_schedule": minutes_until_schedule
    }
    response = requests.post(path, headers=headers, json=payload)
    return response.json()


def get_agent_analytics(region_id: str, project_id: str, agent_id: str, api_key: str, from_date: str = None, to_date: str = None) -> dict:
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/analytics"

    filters = {
        "agentId": {
            "filter_type": "is", # or is_not
            "value": [agent_id] if agent_id else []
        }
    }

    if from_date or to_date:
        filters["insert_date_"] = {
            "filter_type": "date_range",
            "value": {
                "from": from_date or "",
                "to": to_date or ""
            }
        }
    
    payload = {"filters": filters}
    
    response = requests.post(path, headers=headers, json=payload)
    return response.json()
