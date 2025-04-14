from typing import List, Dict, Any
from collections import defaultdict

from agentsmith.utils.data_extractors import extract_tool_runs, extract_tool_data_from_run

def create_simulation_config_from_actions(
    original_actions: List[Dict[str, Any]],
    simulate_unrun_tools: bool = True
) -> Dict[str, Any]:
    """Create a simulation config to replicate tool outputs from original conversation actions.
    
    Args:
        original_actions: The list of actions from the base conversation.
        simulate_unrun_tools: If True, tools not run in the original conversation will execute normally 
                              during replay. If False, they would need a simulation or would fail.
    
    Returns:
        The simulation_config dictionary for trigger_agent_simulation_conversation.
    """
    simulation_config = {"tool_configs": {}}
    tool_run_actions = extract_tool_runs(original_actions)
    
    run_indices: Dict[str, int] = defaultdict(int)
    action_groups: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: {"overrides": {}})

    for action in tool_run_actions:
        tool_data = extract_tool_data_from_run(action)
        if not tool_data or not tool_data.get('action_id'):
            print(f"Warning: Skipping action due to missing tool data/action_id: {action.get('item_id')}")
            continue
            
        action_id = tool_data['action_id']
        output_to_replay = tool_data.get('output')
        state_to_replay = tool_data.get('state')
        
        run_indices[action_id] += 1
        current_run_index = run_indices[action_id]
        
        override_details = {
            "output_overrides_enabled": True,
            "output_overrides": {"output": output_to_replay},
            "action_config_overrides": {
                "action_behaviour": 'never-ask',
                "action_retry_config": {
                    "max_retries": 0,
                    "after_retries_behaviour": "terminate-conversation"
                }
            }
        }

        if state_to_replay == 'error':
            override_details["state_override_enabled"] = True
            override_details["state_override"] = "error"

        action_groups[action_id]["overrides"][str(current_run_index)] = override_details

    simulation_config['tool_configs'] = dict(action_groups)
    return simulation_config

def create_simulation_config_from_manual_overrides(tool_overrides: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create the simulation config JSON based on manually specified overrides.

    Args:
        tool_overrides: A list of dictionaries, each specifying an override.
                         Expected keys per dictionary:
                         - 'action_id': The studio_id of the action (tool) to override.
                         - 'output': The desired output for this override.
                         - 'run_index': (Optional) The 1-based index of the tool call to override.
                                        If omitted or 'default', applies to all runs unless a specific index is matched.
                         - 'state': (Optional) The state to simulate ('finished' or 'error'). Defaults to 'finished'.
    Returns:
        The simulation_config dictionary.
    """
    simulation_config = {"tool_configs": {}}

    action_groups: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: {"overrides": {}})

    for override in tool_overrides:
        action_id = override.get('action_id')
        output_override_ = override.get('output')
        run_index = override.get('run_index', 'default')
        state = override.get('state', 'finished')

        if not action_id:
            continue

        override_details = {
            "output_overrides_enabled": True,
            "output_overrides": {"output": output_override_},
            "action_config_overrides": {
                "action_behaviour": 'never-ask',
                "action_retry_config": {
                    "max_retries": 0,
                    "after_retries_behaviour": "terminate-conversation"
                }
            }
        }

        if state == 'error':
            override_details["state_override_enabled"] = True
            override_details["state_override"] = "error"

        action_groups[action_id]["overrides"][str(run_index)] = override_details

    simulation_config['tool_configs'] = dict(action_groups)
    return simulation_config 