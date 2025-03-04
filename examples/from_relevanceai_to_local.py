from aiworkforce.agent import get_all_agents
from aiworkforce.tool import get_all_tools
from aiworkforce.utils import save_all_objects, update_objects_metadata, remove_objects_changing_fields, remove_local_files_not_in_objects

def get_current_state_from_relevance_ai(region_id, dev_project_id, dev_api_key, prd_project_id):
    # Sync Dev Relevance AI to local
    agents = get_all_agents(region_id, dev_project_id, dev_api_key)
    tools = get_all_tools(region_id, dev_project_id, dev_api_key)
    # knowledge = get_all_knowledge(region_id, dev_project_id, dev_api_key)

    agents = remove_objects_changing_fields(agents)
    tools = remove_objects_changing_fields(tools)
    # knowledge = remove_objects_changing_fields(knowledge)

    agents = update_objects_metadata(agents, prd_project_id)
    tools = update_objects_metadata(tools, prd_project_id)
    # knowledge = update_objects_metadata(knowledge, prd_project_id)

    remove_local_files_not_in_objects(agents, "agents", "relevance_ai/agents")
    save_all_objects(agents, "relevance_ai/agents", "agents")

    remove_local_files_not_in_objects(tools, "tools", "relevance_ai/tools")
    save_all_objects(tools, "relevance_ai/tools", "tools")

    # remove_local_files_not_in_objects(knowledge, "knowledge", "relevance_ai/knowledge")
    # save_all_objects(knowledge, "relevance_ai/knowledge", "knowledge")

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    region_id = os.getenv("region_id")
    dev_project_id = os.getenv("dev_project_id")
    dev_api_key = os.getenv("dev_api_key")
    prd_project_id = os.getenv("prd_project_id")

    get_current_state_from_relevance_ai(region_id, dev_project_id, dev_api_key, prd_project_id)
