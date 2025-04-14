from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class Evaluator(ABC):
    """Abstract base class for all evaluation metrics."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the evaluator."""
        pass

    @abstractmethod
    def evaluate(
        self,
        actions: List[Dict[str, Any]],
        agent_config: Optional[Dict[str, Any]] = None,
        agent_tools_config: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, float]:
        """Compare original and replayed conversations and return metric scores."""
        pass
