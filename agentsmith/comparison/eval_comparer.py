from typing import Dict, Any
from agentsmith.utils.json_utils import json_get

def compare_evaluation_results(
    original_eval: Dict[str, Dict[str, float]],
    replayed_eval: Dict[str, Dict[str, float]]
) -> Dict[str, Any]:
    """Compares evaluation results between an original and a replayed run.

    Args:
        original_eval: The metrics dictionary from evaluating the original run.
                       Structure: {evaluator_name: {metric: score}}
        replayed_eval: The metrics dictionary from evaluating the replayed run.
                       Structure: {evaluator_name: {metric: score}}

    Returns:
        A dictionary containing comparison metrics (e.g., deltas, percentage changes).
    """
    comparison = {"deltas": {}, "notes": []}

    all_evaluator_names = set(original_eval.keys()) | set(replayed_eval.keys())

    for eval_name in all_evaluator_names:
        orig_metrics = original_eval.get(eval_name, {})
        repl_metrics = replayed_eval.get(eval_name, {})
        comparison["deltas"][eval_name] = {}

        all_metric_names = set(orig_metrics.keys()) | set(repl_metrics.keys())

        for metric_name in all_metric_names:
            orig_score = orig_metrics.get(metric_name)
            repl_score = repl_metrics.get(metric_name)

            if orig_score is None and repl_score is None:
                continue # Metric not present in either
            elif orig_score is None:
                comparison["deltas"][eval_name][metric_name] = repl_score
                comparison["notes"].append(f"Metric '{eval_name}.{metric_name}' added in replay.")
            elif repl_score is None:
                comparison["deltas"][eval_name][metric_name] = -orig_score # Indicate removal?
                comparison["notes"].append(f"Metric '{eval_name}.{metric_name}' removed in replay.")
            else:
                # Calculate simple delta
                delta = repl_score - orig_score
                comparison["deltas"][eval_name][metric_name] = delta
                # Optionally add percentage change or other comparison types later

    # Example: Add an overall assessment based on key metrics
    # This needs to be more sophisticated based on which metrics are important
    final_outcome_delta = json_get(comparison, f"deltas.AgentProcedure.final_outcome_success", default=0.0)
    tool_error_delta = json_get(comparison, f"deltas.ToolCalling.tool_errors", default=0.0)
    
    overall_change = "NEUTRAL"
    if final_outcome_delta > 0 and tool_error_delta <= 0: # Improved outcome, errors didn't increase (or decreased)
        overall_change = "IMPROVEMENT"
    elif final_outcome_delta < 0 or tool_error_delta > 0: # Worse outcome or more errors
        overall_change = "REGRESSION"
        
    comparison["overall_assessment"] = overall_change

    return comparison 