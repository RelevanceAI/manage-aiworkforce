from typing import List, Dict, Any, Optional

from agentsmith.evaluation.base import Evaluator
from agentsmith.utils.json_utils import json_get
# from agentsmith.utils.data_extractors import ... # If needed

class AgentProcedureEvaluator(Evaluator):
    """Evaluates the agent's overall workflow effectiveness."""
    @property
    def name(self) -> str:
        return "AgentProcedure"

    def evaluate(
        self,
        actions: List[Dict[str, Any]],
        agent_config: Optional[Dict[str, Any]] = None,
        agent_tools_config: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, float]:
        """Evaluate agent procedure metrics for a single conversation."""
        metrics = {}
        metrics["final_outcome_success"] = self._evaluate_final_outcome(actions)
        metrics["action_advancement"] = self._evaluate_action_advancement(actions)
        metrics["conversation_length"] = float(len(actions))
        return metrics

    def _evaluate_final_outcome(self, actions: List[Dict[str, Any]]) -> float:
        """Evaluate the final state of the conversation. 1.0 if COMPLETED, 0.0 otherwise."""
        if not actions:
            return 0.0
        replayed_state = json_get(actions[-1], 'metadata.conversation.state', 'UNKNOWN')
        return 1.0 if replayed_state == 'COMPLETED' else 0.0

    def _evaluate_action_advancement(self, actions: List[Dict[str, Any]]) -> float:
        """(Placeholder) Evaluate if agent actions progress towards resolving the user's request."""
        # TODO: Implement logic.
        return 0.5
