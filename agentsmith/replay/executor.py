import time
from typing import Optional, List, Dict, Any
import json

from aiworkforce.conversation import trigger_agent_debug_conversation

from agentsmith.utils.loader import load_conversation_actions
from agentsmith.utils.json_utils import json_get

POLLING_INTERVAL_SECONDS = 60
MAX_POLLING_ATTEMPTS = 12

def trigger_replay(
    region_id: str,
    project_id: str,
    agent_id: str,
    trigger_text: str,
    debug_config: Dict[str, Any],
    api_key: str
) -> Optional[str]:
    """Trigger a new conversation in debug mode and return the new conversation ID."""
    try:
        print(f"Triggering replay for agent {agent_id}...")
        trigger_response = trigger_agent_debug_conversation(
            region_id=region_id,
            project_id=project_id,
            agent_id=agent_id,
            trigger_message=trigger_text,
            debug_mode_config=debug_config,
            api_key=api_key
        )
        print(json.dumps(trigger_response, indent=4))
        replayed_id = trigger_response.get('conversation_id')
        if not replayed_id:
            print(f"Error: Could not extract conversation_id from trigger response: {trigger_response}")
            return None
        print(f"Replay triggered. New conversation ID: {replayed_id}")
        return replayed_id
    except Exception as e:
        print(f"Error triggering replay for agent {agent_id}: {e}")
        return None

def await_replay_completion(
    conversation_id: str,
    agent_id: str,
    region_id: str,
    project_id: str,
    api_key: str
) -> Optional[List[Dict[str, Any]]]:
    """Poll the API until the conversation reaches a terminal state and return its actions."""
    attempts = 0
    while attempts < MAX_POLLING_ATTEMPTS:
        print(f"Polling conversation {conversation_id} (Attempt {attempts + 1}/{MAX_POLLING_ATTEMPTS})...")
        from aiworkforce.types import ConversationState
        from aiworkforce.conversation import get_conversations

        # Define non-active states
        active_states = [
            ConversationState.STARTING_UP,
            ConversationState.RUNNING,
            ConversationState.WAITING_FOR_CAPACITY,
            ConversationState.QUEUED_FOR_RERUN
        ]

        conversations_response = get_conversations(region_id, project_id, agent_id, api_key)
        if conversations_response and 'results' in conversations_response:
            conversations = conversations_response['results']

            filtered_conversations = [
                c for c in conversations
                if c.get('knowledge_set') == conversation_id and
                json_get(c, 'metadata.conversation.state') not in active_states
            ]

            if filtered_conversations:
                conversation = filtered_conversations[0]
                state = json_get(conversation, 'metadata.conversation.state')
                print(f"Conversation {conversation_id} finished with state: {state}")
                actions = load_conversation_actions(conversation_id, agent_id, region_id, project_id, api_key)
                return actions

            time.sleep(POLLING_INTERVAL_SECONDS)
            attempts += 1
            continue

    print(f"Error: Conversation {conversation_id} did not complete within the polling timeout.")
    return None
