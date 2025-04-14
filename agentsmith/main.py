import os
import json
from dotenv import load_dotenv

from agentsmith.core.test_runner import TestRunner
from agentsmith.utils.loader import clear_caches
# from agentsmith.comparison import compare_evaluation_results 

load_dotenv()

def run_replay_and_evaluate():
    """Runs a replay of a base conversation and evaluates both runs."""
    REGION_ID = os.getenv("region_id")
    PROJECT_ID = os.getenv("dev_project_id")
    API_KEY = os.getenv("dev_api_key")
    AGENT_ID = os.getenv("dev_agent_id")
    CONVERSATION_ID = os.getenv("dev_conversation_id")

    if not all([REGION_ID, PROJECT_ID, API_KEY, AGENT_ID, CONVERSATION_ID]):
        print("Error: Missing required configuration in .env file.")
        return

    EVALUATORS_TO_RUN = [
        "Setup",
        "ToolCalling", 
        "AgentProcedure",
        # "Hallucination",
        # "Safety",
    ]

    print("--- Starting Agent Simulation --- ")

    print(f"Target Agent ID: {AGENT_ID}")
    print(f"Conversation ID: {CONVERSATION_ID}")
    print(f"Evaluators: {EVALUATORS_TO_RUN}")

    runner = TestRunner(region_id=REGION_ID, project_id=PROJECT_ID, api_key=API_KEY)
    clear_caches()

    results = runner.run_test(
        test_name=f"sim_of_{CONVERSATION_ID}",
        agent_id=AGENT_ID,
        base_conversation_id=CONVERSATION_ID,
        evaluator_names=EVALUATORS_TO_RUN
    )

    if results:
        print("\n--- Final Run Results --- ")
        print(json.dumps(results, indent=2))
    else:
        print("Test run failed or produced no results.")
    print("--- AgentSmith Run Finished --- ")


if __name__ == "__main__":
    run_replay_and_evaluate()
