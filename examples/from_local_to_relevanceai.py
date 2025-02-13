from manage_aiworkforce.agent import create_agent
from manage_aiworkforce.knowledge import create_knowledge
from manage_aiworkforce.tool import create_tools
from manage_aiworkforce.utils import open_all_object_files

def push_to_relevance_ai_prod(region_id, prd_project_id, prd_api_key):
    agents = open_all_object_files("relevance_ai/agents")
    # knowledge = open_all_object_files("relevance_ai/knowledge")
    tools = open_all_object_files("relevance_ai/tools")

    for agent in agents:
        create_agent(agent, region_id, prd_project_id, prd_api_key)

    create_tools(tools, region_id, prd_project_id, prd_api_key)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    region_id = os.getenv("region_id")
    prd_project_id = os.getenv("prd_project_id")
    prd_api_key = os.getenv("prd_api_key")

    push_to_relevance_ai_prod(region_id, prd_project_id, prd_api_key)
