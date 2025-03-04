import requests
import json

from aiworkforce.types import EventType, FilterType, ComparisonType


def get_conversations(region_id:str, project_id:str, agent_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/conversations/list"
    api_params = {
        "page_size": 50000,
        "filters": [{
            "condition": "==",
            "case_insensitive": False,
            "field": "agent_id",
            "filter_type": FilterType.EXACT_MATCH,
            "condition_value": agent_id
        }]
    }
    
    response = requests.get(path, headers=headers, params=json.dumps(api_params))
    return response.json()


def get_conversation_actions(region_id:str, project_id:str, agent_id:str, conversation_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/{agent_id}/tasks/{conversation_id}/view?full_history=true"
    body = {}
    response = requests.post(path, data=json.dumps(body), headers=headers)
    result = response.json()
    if 'results' in result:
        result['results'] = sorted(result['results'], key=lambda x: x.get('insert_date_', ''), reverse=False)
    return result


def get_conversations_where_specific_tool_failed(region_id:str, project_id:str, agent_id:str, tool_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/conversations/list"
    api_params = {
        "page_size": 50000,
        "filters": [{
            "condition": "==",
            "case_insensitive": False,
            "field": "agent_id",
            "filter_type": FilterType.EXACT_MATCH,
            "condition_value": agent_id
        }],
        "event_logs_filters": [{
            "event_value": tool_id,
            "event_type": EventType.TOOL_RUNS_FAILED,
            "min_count": 1,
            "max_count": 10,
            "comparison_type": ComparisonType.GTE
        }]
    }
    response = requests.get(path, headers=headers, params=json.dumps(api_params))
    return response.json()


def retrigger_conversation_after_message(project_id:str, region_id:str, agent_id:str, conversation_id:str, message_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/trigger"

    payload = {
        "action": "regenerate",
        "regenerate_message_id": message_id,
        "agent_id": agent_id,
        "conversation_id": conversation_id,
    }

    response = requests.post(path, headers=headers, json=payload)
    return response.json()

