from typing import List, Dict, Any, Optional

from agentsmith.evaluation.base import Evaluator

class SetupEvaluator(Evaluator):
    """Evaluates the agent's setup/configuration quality."""
    # Note: This evaluator likely needs access to the agent's configuration
    # data (instructions, tool settings) beyond just conversation actions.
    # The evaluate signature might need adjustment or the TestRunner
    # might need to pass agent config data.
    @property
    def name(self) -> str:
        return "Setup"

    def evaluate(
        self,
        original_actions: List[Dict[str, Any]],
        agent_config: Optional[Dict[str, Any]] = None,
        agent_tools_config: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, float]:
        """Evaluate setup metrics. Requires agent_config and optionally agent_tools_config."""
        if agent_config is None:
             print(f"Warning: {self.name} requires agent_config, which was not provided. Skipping.")
             return {
                "instructions_quality": 0.0,
                "tools_config_quality": 0.0,
                "complexity": 0.0
            }

        metrics = {}
        metrics["instructions_quality"] = self._evaluate_instructions(agent_config)
        metrics["tools_config_quality"] = self._evaluate_tools_config(agent_config, agent_tools_config)
        metrics["complexity"] = self._evaluate_complexity(agent_config, agent_tools_config)
        return metrics

    def _evaluate_instructions(self, agent_config: Dict[str, Any]) -> float:
        """Evaluate instruction quality based on length."""
        # Simple metric: Score based on length (e.g., 1.0 if > 100 chars, 0.0 otherwise)
        # More complex logic could involve LLM analysis for clarity, keyword checks etc.
        instructions = agent_config.get('system_prompt', '') # Use 'system_prompt' based on agents.json
        if not isinstance(instructions, str):
            return 0.0 # Invalid instructions format
        
        # Example scoring: Penalize very short or excessively long prompts
        length = len(instructions)
        if 100 < length < 5000:
             score = 1.0
        elif 50 < length <= 100 or 5000 <= length < 10000:
             score = 0.5
        else:
             score = 0.1 # Very short or extremely long
        return score

    def _evaluate_tools_config(self, agent_config: Dict[str, Any], agent_tools_config: Optional[List[Dict[str, Any]]]) -> float:
        """Evaluate tool configuration quality."""
        # Simple metric: Score based on presence and number of tools
        # Could check for duplicate tool IDs, use agent_tools_config for deeper analysis if available.
        agent_actions = agent_config.get('actions', [])
        if not isinstance(agent_actions, list):
            return 0.0 # Invalid actions format

        num_tools = len(agent_actions)
        if num_tools == 0:
            return 0.0 # No tools configured
        
        # Check for duplicate action IDs (chain_id or agent_id)
        action_ids = set()
        has_duplicates = False
        for action in agent_actions:
            action_id = action.get('chain_id') or action.get('agent_id')
            if action_id:
                if action_id in action_ids:
                    has_duplicates = True
                    break
                action_ids.add(action_id)

        if has_duplicates:
            return 0.2 # Penalize duplicate tool registrations
        
        # Score based on number of tools (example: peak at 3-7 tools)
        if 3 <= num_tools <= 7:
            score = 1.0
        elif 1 <= num_tools < 3 or 7 < num_tools <= 10:
            score = 0.7
        else: # < 1 or > 10
            score = 0.4
            
        # TODO: Add checks using agent_tools_config if available (e.g., schema validity, description presence)
        return score

    def _evaluate_complexity(self, agent_config: Dict[str, Any], agent_tools_config: Optional[List[Dict[str, Any]]]) -> float:
        """Estimate agent complexity based on instructions and tools."""
        instruction_score = self._evaluate_instructions(agent_config)
        tools_score = self._evaluate_tools_config(agent_config, agent_tools_config)
        num_tools = len(agent_config.get('actions', []))
        
        # Simple weighted average - adjust weights as needed
        # Higher instruction score and moderate tool count contribute positively
        complexity_score = (0.4 * instruction_score) + (0.6 * tools_score)
        
        # Penalize very high number of tools further
        if num_tools > 10:
            complexity_score *= 0.7
        elif num_tools > 15:
             complexity_score *= 0.4
             
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, complexity_score))
