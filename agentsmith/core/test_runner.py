import json
from typing import Dict, Any, List, Optional

from agentsmith.core.tool_simulator import create_simulation_config_from_actions
from agentsmith.core.metrics import MetricsCollector
from agentsmith.utils.data_extractors import extract_trigger_message
from agentsmith.evaluation import load_evaluator
from agentsmith.utils.loader import (
    load_agent_config,
    load_agent_tools_config,
    load_conversation_actions
)
from agentsmith.replay.executor import trigger_replay, await_replay_completion
from agentsmith.comparison import compare_evaluation_results

class TestRunner:
    """Orchestrates agent test execution by coordinating data loading, replay, and evaluation."""

    def __init__(
        self,
        region_id: str,
        project_id: str,
        api_key: str,
        metrics_collector: Optional[MetricsCollector] = None
    ):
        """Initialize TestRunner with necessary credentials."""
        self.region_id = region_id
        self.project_id = project_id
        self.api_key = api_key
        self.metrics_collector = metrics_collector or MetricsCollector()

    def _run_evaluations(
        self,
        evaluator_names: List[str],
        original_actions: Optional[List[Dict[str, Any]]],
        replayed_actions: Optional[List[Dict[str, Any]]],
        agent_config: Optional[Dict[str, Any]],
        agent_tools_config: Optional[List[Dict[str, Any]]]
    ) -> None:
        """Load and run the specified evaluators for both original and replayed runs."""
        print(f"Running evaluators: {evaluator_names}")

        # Evaluate original run (if available)
        if original_actions:
            print("Evaluating original conversation...")
            self.metrics_collector.start_run() # Start a run for original
            for name in evaluator_names:
                evaluator = load_evaluator(name)
                if evaluator:
                    try:
                        metrics = evaluator.evaluate(
                            original_actions,
                            agent_config=agent_config,
                            agent_tools_config=agent_tools_config
                        )
                        self.metrics_collector.add_result(evaluator.name, metrics)
                    except Exception as e:
                        print(f"Error running evaluator '{evaluator.name}' on original: {e}")
                        self.metrics_collector.add_result(evaluator.name, {"evaluation_error": 1.0})
            self.metrics_collector.end_run("original") # End run, name it 'original'
        else:
            print("Skipping evaluation of original conversation (not available).")

        # Evaluate replayed run (if available)
        if replayed_actions:
            print("Evaluating replayed conversation...")
            self.metrics_collector.start_run() # Start a run for replayed
            for name in evaluator_names:
                evaluator = load_evaluator(name)
                if evaluator:
                    try:
                        metrics = evaluator.evaluate(
                            replayed_actions,
                            agent_config=agent_config,
                            agent_tools_config=agent_tools_config
                        )
                        self.metrics_collector.add_result(evaluator.name, metrics)
                    except Exception as e:
                        print(f"Error running evaluator '{evaluator.name}' on replay: {e}")
                        self.metrics_collector.add_result(evaluator.name, {"evaluation_error": 1.0})
            self.metrics_collector.end_run("replayed") # End run, name it 'replayed'
        else:
            print("Skipping evaluation of replayed conversation (not available).")

    def get_data(
        self,
        agent_id: str,
        conversation_id: str
    ) -> Optional[Dict[str, Any]]:
        """Load data for a given agent and conversation."""
        agent_config = load_agent_config(agent_id, self.region_id, self.project_id, self.api_key)
        agent_tools_config = load_agent_tools_config(agent_id, self.region_id, self.project_id, self.api_key)
        original_actions = load_conversation_actions(conversation_id, agent_id, self.region_id, self.project_id, self.api_key)

        if not original_actions:
            print(f"Error: Failed to fetch original conversation actions for {conversation_id}. Cannot proceed with replay.")
            return None # Cannot replay without original

        trigger_message = extract_trigger_message(original_actions or [])
        if not trigger_message:
            print(f"Error: Could not find trigger message in conversation {conversation_id}. Cannot proceed with replay.")
            return None

        return {
            'agent_config': agent_config,
            'agent_tools_config': agent_tools_config,
            'original_actions': original_actions,
            'trigger_message': trigger_message
        }


    def run_simulation_conversation(
        self,
        agent_id: str,
        trigger_message: str,
        simulation_config: Dict[str, Any],
        test_name: str
    ) -> Optional[Dict[str, Any]]:
        """Run a debug conversation."""
        # Execute replay
        replayed_actions: Optional[List[Dict[str, Any]]] = None

        replayed_conversation_id = trigger_replay(
            self.region_id, self.project_id, agent_id,
            trigger_message, simulation_config, self.api_key
        )

        if not replayed_conversation_id:
            print("Error: Failed to trigger replay.")
            # Record framework error
            self.metrics_collector.start_run()
            self.metrics_collector.add_result("Framework", {"run_status": 0.0, "error": "Trigger failed"})
            self.metrics_collector.end_run(test_name)
            return None

        replayed_actions = await_replay_completion(
            replayed_conversation_id, agent_id, self.region_id, self.project_id, self.api_key
        )
        if replayed_actions:
            print(f"Replayed conversation fetched ({len(replayed_actions)} actions).")

        if not replayed_actions:
            print(f"Error: Failed to fetch completed replayed conversation actions for {replayed_conversation_id}.")
            # Record framework error
            self.metrics_collector.start_run()
            self.metrics_collector.add_result("Framework", {"run_status": 0.0, "error": "Polling failed"})
            self.metrics_collector.end_run(test_name)
            return None

        return replayed_actions


    def run_test(
        self,
        test_name: str,
        agent_id: str,
        base_conversation_id: str,
        evaluator_names: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Run a single test case based on provided parameters."""
        print(f"\n--- Running Test: {test_name} ---")
        # Prepare for replay
        data = self.get_data(agent_id, base_conversation_id)
        if not data:
            print("Skipping test due to missing data.")
            return None

        simulation_config = {}
        if data['original_actions']:
            simulation_config = create_simulation_config_from_actions(data['original_actions'])
            print(f"Generated dynamic simulation config based on {len(simulation_config.get('tool_configs', {}))} tools run in original.")
        else:
             print("Skipping dynamic simulation config generation (no original actions).")

        replayed_actions = self.run_simulation_conversation(
            agent_id,
            data['trigger_message']['text'],
            simulation_config,
            test_name
        )

        # Run Evaluations (always run, evaluators handle missing data)
        self._run_evaluations(
            evaluator_names,
            data['original_actions'],
            replayed_actions,
            data['agent_config'],
            data['agent_tools_config']
        )

        self.metrics_collector.end_run(test_name)        
        all_eval_results = dict(self.metrics_collector.test_run_results) # Get all stored runs
        self.metrics_collector.test_run_results.clear() # Clear collector for next test

        print(f"--- Test {test_name} Completed ---")
        print("Individual Run Evaluation Results:")
        print(json.dumps(all_eval_results, indent=2))

        # Perform comparison if both original and replayed results exist
        comparison_summary = None
        original_eval = all_eval_results.get('original')
        replayed_eval = all_eval_results.get('replayed')

        if original_eval and replayed_eval:
            print("\nComparing original vs. replayed results...")
            comparison_summary = compare_evaluation_results(original_eval[0], replayed_eval[0]) # Assuming one run per key
            print("Comparison Summary:")
            print(json.dumps(comparison_summary, indent=2))
        else:
            print("\nSkipping comparison (missing original or replayed evaluation results).")

        # Return a combined dictionary
        final_output = {
            "test_name": test_name,
            "evaluations": all_eval_results,
            "comparison": comparison_summary
        }
        return final_output
