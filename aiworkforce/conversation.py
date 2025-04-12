import requests
import json
from datetime import datetime, timedelta

import pytz

from aiworkforce.types import EventType, FilterType, ComparisonType


def get_conversations(region_id:str, project_id:str, agent_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/conversations/list"
    api_params = {
        "include_agent_details": "true",
        "include_debug_info": "false",
        "filters": json.dumps(
            [
                {
                    "field": "conversation.is_debug_mode_task",
                    "filter_type": FilterType.EXACT_MATCH,
                    "condition": "!=",
                    "condition_value": True,
                },
                {
                    "filter_type": FilterType.EXACT_MATCH,
                    "field": "conversation.agent_id",
                    "condition_value": agent_id,
                    "condition": "==",
                },
            ]
        ),
        "sort": json.dumps([{"update_datetime": "desc"}]),
        "page_size": 500000,
    }
    
    response = requests.get(path, headers=headers, params=json.dumps(api_params))
    return response.json()


def get_list_conversation_studio_history(region_id:str, project_id:str, api_key:str, agent_id:str, conversation_id:str, page_size:int=500000, page:int=1):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/conversations/studios/list"
    
    params = {
        "agent_id": agent_id,
        "conversation_id": conversation_id,
        "page_size": page_size,
        "page": page
    }

    response = requests.get(path, headers=headers, params=params)
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

def trigger_agent_debug_conversation(region_id: str, project_id: str, agent_id: str, trigger_message: str, debug_mode_config: dict, api_key: str) -> dict:
    """Trigger conversation in debug mode """
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/trigger"
    payload = {
        "agent_id": agent_id,
        "message": {
                "role": "user",
                "content": trigger_message,
            },
        "debug": True, 
        "is_debug_mode_task": True,
        "debug_mode_config": debug_mode_config
    }
    # ,
    #     "agent_override": {
    #         "model": "openai-gpt-4o-mini",
    #         "title_prompt": "",
    #         "system_prompt": ""
    #     }
    response = requests.post(path, headers=headers, json=payload)
    return response.json()

def get_trigger_message(region_id:str, project_id:str, agent_id:str, conversation_id:str, api_key:str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/{agent_id}/tasks/{conversation_id}/trigger_message"
    
    response = requests.get(path, headers=headers)
    trigger_message_data = response.json().get("trigger_message")
    
    if trigger_message_data and trigger_message_data.get("content", {}).get("is_trigger_message", False):
        return {
          "conversation_id": conversation_id,
          "message_id": trigger_message_data["item_id"],
          "message": trigger_message_data["content"]["text"],
          "triggered_by": trigger_message_data.get('content', {}).get('display', {}).get('name', None)
        }
    return {}


def get_conversations_where_specific_tool_failed(region_id:str, project_id:str, agent_id:str, tool_id:str, api_key:str):
    """ Variation of get_conversations with advanced filters """
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/conversations/list"
    api_params = {
        "page_size": 50000,
        "filters": json.dumps([{
            "condition": "==",
            "case_insensitive": False,
            "field": "agent_id",
            "filter_type": FilterType.EXACT_MATCH,
            "condition_value": agent_id
        }]),
        "event_logs_filters": json.dumps([{
            "event_value": tool_id,
            "event_type": EventType.TOOL_RUNS_FAILED,
            "min_count": 1,
            "max_count": 10,
            "comparison_type": ComparisonType.GTE
        }])
    }
    response = requests.get(path, headers=headers, params=api_params)
    return response.json()


def get_conversations_between_dates(region_id, project_id, agent_id, api_key, from_dt=None, to_dt=None):
    """ Variation of get_conversations with advanced filters """
    headers = {"Authorization": f"{project_id}:{api_key}", "Content-Type": "application/json"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/agents/conversations/list"

    filters = [
        {
            "field": "conversation.is_debug_mode_task",
            "filter_type": "exact_match",
            "condition": "!=",
            "condition_value": True
        },
        {
            "filter_type": "exact_match",
            "field": "conversation.agent_id",
            "condition_value": [agent_id],
            "condition": "=="
        }
    ]
    # has to be in these exact formats
    if from_dt:
        filters.append({
            "filter_type": "numeric",
            "field": "update_datetime",
            "condition": ">=",
            "condition_value": from_dt.astimezone(pytz.timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        })
    if to_dt:
        filters.append({
            "filter_type": "numeric",
            "field": "update_datetime",
            "condition": "<",
            "condition_value": (to_dt + timedelta(days=1)).astimezone(pytz.timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        })
  
    params = {
        "include_agent_details": "false",
        "include_debug_info": "false",
        "filters": json.dumps(filters),
        "sort": json.dumps([{"update_datetime": "desc"}]),
        "page_size": 500000
    }
    
    response = requests.get(path, params=params, headers=headers)
    return response.json()
