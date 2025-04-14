# Expose Evaluator classes and the loader function
from .base import Evaluator
from .hallucination_evaluator import HallucinationEvaluator
from .safety_evaluator import SafetyEvaluator
from .tool_calling_evaluator import ToolCallingEvaluator
from .agent_procedure_evaluator import AgentProcedureEvaluator
from .setup_evaluator import SetupEvaluator

from typing import Optional, Type, Dict, List

# Auto-discover subclasses of Evaluator from the imported modules
# Ensure all evaluator modules are imported above
_evaluator_classes: Dict[str, Type[Evaluator]] = {
    cls().name: cls
    for cls in Evaluator.__subclasses__()
}

def load_evaluator(name: str) -> Optional[Evaluator]:
    """Load an evaluator instance by its name."""
    cls = _evaluator_classes.get(name)
    if cls:
        return cls()
    print(f"Warning: Evaluator '{name}' not found.")
    return None

def list_available_evaluators() -> List[str]:
    """Return a list of names of available evaluators."""
    return list(_evaluator_classes.keys())

__all__ = [
    'Evaluator',
    'HallucinationEvaluator',
    'SafetyEvaluator',
    'ToolCallingEvaluator',
    'AgentProcedureEvaluator',
    'SetupEvaluator',
    'load_evaluator',
    'list_available_evaluators'
] 