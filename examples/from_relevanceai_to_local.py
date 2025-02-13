from manage_aiworkforce.agent import get_all_agents, get_agent_tools
from manage_aiworkforce.knowledge import get_all_knowledge
from manage_aiworkforce.tool import get_all_tools
from manage_aiworkforce.utils import save_all_objects, update_objects_metadata, remove_objects_changing_fields, remove_local_files_not_in_objects

def get_current_state_from_relevance_ai():
    
    agents = get_all_agents(region_id, dev_project_id, dev_api_key)
    agents = remove_objects_changing_fields(agents)
    agents = update_objects_metadata(agents, prd_project_id)

    remove_local_files_not_in_objects(agents, "agents", "relevance_ai/agents")
    save_all_objects(agents, "relevance_ai/agents", "agents")


if __name__ == "__main__":
    get_current_state_from_relevance_ai()
