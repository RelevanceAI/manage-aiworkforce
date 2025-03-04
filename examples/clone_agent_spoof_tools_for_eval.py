import os
from dotenv import load_dotenv

from aiworkforce.agent import get_all_agents, get_agent_tools, create_agent
from aiworkforce.tool import create_tools
from aiworkforce.utils import update_objects_metadata, remove_objects_changing_fields
from aiworkforce.evaluation.spoof import spoof_tools


def recreate_agent(agent, tools, region_id, eval_project_id, eval_api_key):
    create_agent(agent, region_id, eval_project_id, eval_api_key)
    create_tools(tools, region_id, eval_project_id, eval_api_key)


def get_agent_and_tools(region_id, source_project_id, agent_id, source_api_key, eval_project_id):
    agents = get_all_agents(region_id, source_project_id, source_api_key)
    agent = next((a for a in agents if a['agent_id'] == agent_id), None)

    tools = get_agent_tools(agent_id, region_id, source_project_id, api_key)

    agent = remove_objects_changing_fields([agent])
    tools = remove_objects_changing_fields(tools)
    agent = update_objects_metadata([agent], eval_project_id)
    tools = update_objects_metadata(tools, eval_project_id)
    return agent, tools


if __name__ == "__main__":

    load_dotenv()

    region_id = os.getenv("region_id")
    dev_project_id = os.getenv("dev_project_id")
    dev_api_key = os.getenv("dev_api_key")
    prd_project_id = os.getenv("prd_project_id")

    agent, tools = get_agent_and_tools(region_id, dev_project_id, agent_id, dev_api_key, prd_project_id)
    tools = spoof_tools(tools)

    prd_api_key = os.getenv("prd_api_key")
    recreate_agent(agent, tools, region_id, prd_project_id, prd_api_key)

