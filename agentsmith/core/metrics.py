from typing import Dict, List, Any
from collections import defaultdict

class MetricsCollector:
    """Collects and aggregates evaluation metrics from multiple sources for test runs."""

    def __init__(self):
        # Stores results per test run
        # Structure: {test_name: [{evaluator_name: {metric: score}}]}
        self.test_run_results: Dict[str, List[Dict[str, Dict[str, float]]]] = defaultdict(list)
        self._current_run_metrics: Dict[str, Dict[str, float]] = {}

    def start_run(self) -> None:
        """Reset metrics for the start of a new evaluation run."""
        self._current_run_metrics = defaultdict(dict)

    def add_result(self, evaluator_name: str, metrics: Dict[str, float]) -> None:
        """Add metrics from a specific evaluator for the current run."""
        if not isinstance(metrics, dict):
            # print(f"Warning: Metrics from {evaluator_name} are not a dict: {metrics}")
            return
        self._current_run_metrics[evaluator_name].update(metrics)

    def end_run(self, test_name: str) -> None:
        """Finalize the current run and store its results."""
        if self._current_run_metrics:
            self.test_run_results[test_name].append(dict(self._current_run_metrics))
        self.start_run() # Reset for the next potential run

    def get_run_results(self, test_name: str) -> List[Dict[str, Dict[str, float]]]:
        """Get all recorded results for a specific test name."""
        return self.test_run_results.get(test_name, [])

    def get_latest_run_summary(self, test_name: str) -> Dict[str, Any]:
        """Get a summary of the latest run for a specific test."""
        runs = self.get_run_results(test_name)
        if not runs:
            return {"error": f"No runs found for test '{test_name}'"}

        latest_run = runs[-1]
        summary = {
            'evaluators': list(latest_run.keys()),
            'metrics': latest_run,
            'overall_score': self._calculate_overall_score(latest_run) # Example aggregation
        }
        return summary

    def get_all_test_summaries(self) -> Dict[str, Dict[str, Any]]:
         """Get summaries for the latest run of all tests."""
         return {test_name: self.get_latest_run_summary(test_name) for test_name in self.test_run_results}

    def _calculate_overall_score(self, run_metrics: Dict[str, Dict[str, float]]) -> float:
        """Calculate a simple overall score (e.g., average). Needs refinement."""
        all_scores = []
        for evaluator_metrics in run_metrics.values():
            all_scores.extend(evaluator_metrics.values())

        if not all_scores:
            return 0.0
        # Simple average for now. Could be weighted later.
        return sum(all_scores) / len(all_scores)

    # TODO: Add methods for historical trend analysis if needed. 
