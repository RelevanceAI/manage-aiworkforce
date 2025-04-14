from typing import Any, List, Dict, Optional

from agentsmith.utils.json_utils import json_get

def extract_trigger_message(conversation_actions: List[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    """Extract the trigger message from conversation actions using json_get."""
    for action in conversation_actions:
        if json_get(action, 'content.is_trigger_message', default=False):
            text = json_get(action, 'content.text', default='')
            message_id = json_get(action, 'item_id', default='')
            return {
                'text': text,
                'message_id': message_id
            }
    return None

def extract_tool_runs(conversation_actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract all tool run steps from conversation actions."""
    tool_runs = []
    for action in conversation_actions:
        if json_get(action, 'content.type') == 'tool-run':
            tool_runs.append(action)
    return tool_runs

def extract_tool_data_from_run(tool_run_action: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract key data points from a single tool run action."""
    action_id = json_get(tool_run_action, 'content.action_details.action')
    tool_id = json_get(tool_run_action, 'content.tool_config.id')
    tool_title = json_get(tool_run_action, 'content.tool_config.title')
    state = json_get(tool_run_action, 'content.tool_run_state')
    output = None

    if not action_id or not tool_id or not state:
        # Essential data missing, cannot process this run
        return None

    if state == 'finished':
        output = json_get(tool_run_action, 'content.output')
    elif state == 'error':
        errors = json_get(tool_run_action, 'content.errors', default=[])
        if errors and isinstance(errors, list):
            first_error = errors[0]
            output = json_get(first_error, 'raw', default=json_get(first_error, 'body', default=first_error))
        else:
            output = "Unknown error structure"
    else:
        # Handle other states like 'running', 'pending' if necessary, or ignore
        pass

    return {
        'action_id': action_id,
        'tool_id': tool_id,
        'tool_title': tool_title,
        'state': state,
        'output': output,
        'original_action': tool_run_action
    }
