# Manage Your AI Workforce
Designed to allow Relevance AI users to manage their Relevance AI environments locally and deploy from files or Git to any Relevance AI project.

*Note: This codebase is not designed to be used as a package or imported into your project. Use these functions as your building blocks to create your CI-CD pipelines.*

## Usage

The package can be used in two major ways:

### 1. Exporting your assets from a Relevance AI project to Local Files

The example script `examples/from_relevanceai_to_local.py` fetches agents and tools (with optional support for knowledge sets) from your Relevance AI project and writes them to local JSON files. This helps you:

### 2. Pushing Local file assets to a Relevance AI project

The example script `examples/from_local_to_relevanceai.py` reads local JSON files (for agents and tools) and pushes them to your production Relevance AI environment. This is useful for:

## API Functions

The package provides core functions to interact directly with the Relevance AI API:

- **Agents**
  - `get_all_agents`
  - `create_agent`
  - `get_agent_tools`
  
- **Knowledge**
  - `get_all_knowledge`
  - `get_knowledge`
  - `create_knowledge`
  - `delete_knowledge`
  - `get_knowledge_metadata`
  
- **Tools**
  - `get_all_tools`
  - `create_tools`
  - `delete_tools`
  
- **Utility Functions**
  - File I/O helpers like `open_all_object_files` and `save_all_objects` for local file management.
  - Functions to clean and update metadata to ensure consistency between environments.

## Contributing

Contributions to enhance features or extend functionality are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

---

Manage your environment seamlessly with manage-aiworkforce.
