# Manage Your AI Workforce
Designed to allow Relevance AI users to manage their Relevance AI environments locally and deploy from files or Git to any Relevance AI project.

*Note: This codebase is not designed to be used as a package or imported into your project. Use these functions as your building blocks to create your CI-CD pipelines.*

## Usage

The package can be used in two major ways:

### 1. Exporting your assets from a Relevance AI project to Local Files

The example script `examples/from_relevanceai_to_local.py` fetches agents and tools (with optional support for knowledge sets) from your Relevance AI project and writes them to local JSON files. This helps you:

### 2. Pushing Local file assets to a Relevance AI project

The example script `examples/from_local_to_relevanceai.py` reads local JSON files (for agents and tools) and pushes them to your production Relevance AI environment. This is useful for:

### 3. Retrigger Failed Conversations

The example script `examples/trigger_conversations_from_failure.py` shows how you can identify and regenerate conversations that have errored, starting them from just before the last error.

### 4. Agent costs of past conversations between a given timeframe.

The example script `examples/get_agent_conversation_costs.py` calculates the costs of past conversations for a given agent within a specified timeframe. This is useful for understanding the cost distribution and usage patterns of your agents over time. Note: May not properly count subagents' costs.

## API Functions

The package provides core functions to interact directly with the Relevance AI API:
- **Agents**
  - `get_all_agents`
  - `create_agent`
  - `get_agent_tools`
  - `delete_agent`
  - `update_agent`
  - `schedule_message_to_agent`
  - `get_agent_analytics`
  - `save_agents_to_file`

- **Knowledge**
  - `get_all_knowledge`
  - `get_knowledge`
  - `delete_knowledge`
  - `add_knowledge_data`
  - `get_knowledge_metadata`

- **Tools**
  - `get_tool`
  - `get_all_tools`
  - `create_tools`
  - `delete_tools`
  - `get_tool_run_history`
  - `trigger_tool`
  - `poll_tool_run`
  - `update_tool`
  - `save_tools_to_file`

- **Conversations**
  - `get_conversations`
  - `get_list_conversation_studio_history`
  - `get_conversation_actions`
  - `retrigger_conversation_after_message`
  - `trigger_agent_debug_conversation`
  - `get_trigger_message`
  - `get_conversations_where_specific_tool_failed`
  - `get_conversations_between_dates`

- **Snippets**
  - `upsert_snippet`

## Contributing

Contributions to enhance features or extend functionality are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

---

Manage your environment seamlessly with manage-aiworkforce.
