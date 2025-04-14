from typing import List, Dict, Any, Optional

from agentsmith.evaluation.base import Evaluator
from agentsmith.utils.json_utils import json_get
from agentsmith.utils.data_extractors import extract_tool_runs, extract_tool_data_from_run

class ToolCallingEvaluator(Evaluator):
    """Evaluates the quality of tool usage within a single conversation."""
    @property
    def name(self) -> str:
        return "ToolCalling"

    def evaluate(
        self,
        actions: List[Dict[str, Any]],
        agent_config: Optional[Dict[str, Any]] = None,
        agent_tools_config: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, float]:
        """Evaluate tool calling metrics for a single conversation."""
        tool_run_actions = extract_tool_runs(actions)
        tool_data_list = [
            d for act in tool_run_actions if (d := extract_tool_data_from_run(act))
        ]

        metrics = {}
        metrics["tool_count"] = self._evaluate_tool_count(tool_data_list)
        metrics["tool_errors"] = self._evaluate_tool_errors(tool_data_list)
        metrics["avg_input_complexity"] = self._evaluate_avg_input_complexity(tool_run_actions, agent_tools_config)

        return metrics

    def _evaluate_tool_count(self, tool_data_list: List[Dict]) -> float:
        """Return the number of tool calls made."""
        return float(len(tool_data_list))

    def _evaluate_tool_errors(self, tool_data_list: List[Dict]) -> float:
        """Calculate the fraction of tool calls that resulted in an error."""
        if not tool_data_list:
            return 0.0 # Or 1.0 if no calls implies no errors?
        errors = sum(1 for d in tool_data_list if d.get('state') == 'error')
        return float(errors) / len(tool_data_list)

    def _evaluate_avg_input_complexity(self, tool_run_actions: List[Dict], agent_tools_config: Optional[List[Dict]]) -> float:
        """(Placeholder) Calculate average complexity of tool inputs."""
        # TODO: Implement logic. Could count number of args, check types, etc.
        # Requires agent_tools_config to map action_id to params_schema.
        if not tool_run_actions:
            return 0.0
        # Placeholder: just count average number of top-level keys in input args
        total_args = 0
        for action in tool_run_actions:
            args = json_get(action, 'content.input.arguments', default={})
            if isinstance(args, dict):
                total_args += len(args.keys())
        return float(total_args) / len(tool_run_actions)

    # Removed methods that compared two runs (_evaluate_selection_quality, previous _evaluate_input_quality)
