from manage_aiworkforce.agent import create_agent
from manage_aiworkforce.tool import create_tools
from manage_aiworkforce.utils import open_all_object_files

def push_to_relevance_ai_prod():

    agents = open_all_object_files("relevance_ai/agents")
    # knowledge = open_all_object_files("relevance_ai/knowledge")
    tools = open_all_object_files("relevance_ai/tools")

    for agent in agents:
        create_agent(agent, region_id, prd_project_id, prd_api_key)

    create_tools(tools, region_id, prd_project_id, prd_api_key)


if __name__ == "__main__":
    push_to_relevance_ai_prod()
