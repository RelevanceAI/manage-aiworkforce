from typing import Optional, Dict, List, Any

from aiworkforce.agent import get_all_agents, get_agent_tools
from aiworkforce.conversation import get_conversation_actions


def load_agent_config(
    agent_id: str,
    region_id: str,
    project_id: str,
    api_key: str
) -> Optional[Dict[str, Any]]:
    """Load agent configuration data."""
    try:
        print(f"Fetching agent config: {agent_id}")
        agents = get_all_agents(region_id, project_id, api_key)
        for agent in agents:
            if agent['agent_id'] == agent_id:
                config = agent
                return config
        return None
    except Exception as e:
        print(f"Error fetching agent config for {agent_id}: {e}")
        return None


def load_agent_tools_config(
    agent_id: str,
    region_id: str,
    project_id: str,
    api_key: str
) -> Optional[List[Dict[str, Any]]]:
    """Load detailed configuration for all tools associated with an agent."""
    try:
        print(f"Fetching agent tools config: {agent_id}")
        tools_config = get_agent_tools(agent_id, region_id, project_id, api_key)
        return tools_config
    except Exception as e:
        print(f"Error fetching agent tools config for {agent_id}: {e}")
        return None


def load_conversation_actions(
    conversation_id: str,
    agent_id: str,
    region_id: str,
    project_id: str,
    api_key: str,
) -> Optional[List[Dict[str, Any]]]:
    """Load all actions for a specific conversation."""
    try:
        print(f"Fetching conversation actions: {conversation_id}")
        return get_conversation_actions(region_id, project_id, agent_id, conversation_id, api_key)['results']
    except Exception as e:
        print(f"Error fetching conversation actions for {conversation_id}: {e}")
        return None
