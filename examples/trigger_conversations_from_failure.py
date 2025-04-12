import os
import time
from dotenv import load_dotenv

from manage_aiworkforce.types import ConversationState
from manage_aiworkforce.conversation import get_conversations, retrigger_conversation_after_message, get_conversation_actions


if __name__ == "__main__":
    # Explanation and demo video: https://www.loom.com/share/a1204a2f13964c4284b391a590502bf7?sid=b7cd34ce-f1e0-47d9-9cf4-14799abd8105
    load_dotenv()
    region_id = os.getenv("region_id")
    project_id = os.getenv("dev_project_id")
    agent_id = os.getenv("dev_agent_id")
    api_key = os.getenv("dev_api_key")

    error_states = [
        ConversationState.ERRORED_PENDING_APPROVAL,
        ConversationState.UNRECOVERABLE,
        ConversationState.TIMED_OUT
    ]

    # STEP 1: Get failed conversation metadata
    # NOTE: can't get conversation filters to work, so simply get all and filter afterwards
    conversations = get_conversations(region_id, project_id, agent_id, api_key).get('results', [])
    failed_conversations = [c for c in conversations if c.get('metadata', {}).get('conversation', {}).get('state', '') in error_states]

    for conversation_metadata in failed_conversations:
        # STEP 2: Get the conversation messages (actions)
        conversation_id = conversation_metadata.get('knowledge_set', None)
        conversation = get_conversation_actions(region_id, project_id, agent_id, conversation_id, api_key).get('results', [])

        # STEP 3: Find the message ID of the action-response 1 before the last action-error
        prev_event_id = None
        for i in range(len(conversation) - 1, -1, -1):
            if conversation[i].get('content', {}).get('tool_run_state', '') == 'error':
                prev_event_ids = conversation[i - 1].get('content', {}).get('original_message_ids', {})
                # Get the last id from the previous event
                prev_event_id = prev_event_ids.get('action-response', prev_event_ids.get('action-error', prev_event_ids.get('agent-error', conversation[i - 1].get('content', {}).get('item_id', None))))
                if prev_event_id is not None:
                    break
        if prev_event_id is None:
            print(f"No failed tool run state was found, skipping conversation: {conversation_id} with state: {conversation_metadata.get('metadata', {}).get('conversation', {}).get('state', '')}")
            continue

        # STEP 4: Trigger the conversation from the message ID
        print(f"Triggering conversation {conversation_id} from after message ID: {prev_event_id}")
        _ = retrigger_conversation_after_message(project_id, region_id, agent_id, conversation_id, prev_event_id, api_key)
        # STEP 5: Add a delay to not get rate limited...
        # NOTE: You can trigger all the conversations at once without the API returning a rate limit error
        # However, internal tools the agent is using (such as API calls or LLM queries) including the agent itself, may through a rate limit error during runtime.
        time.sleep(20)
