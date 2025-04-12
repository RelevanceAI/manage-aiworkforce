import statistics as stats
import pytz
from datetime import datetime, timedelta
from collections import Counter

from aiworkforce.conversation import get_conversations_between_dates, get_list_conversation_studio_history


def str_to_datetime(date_string, from_tz='UTC', to_tz='Australia/Sydney'):
    if not date_string:
        return None
    if 'T' not in date_string:
        date_string = f"{date_string}T00:00:00"
    if '.' in date_string:
        date_string = date_string.split('.')[0]
    
    if date_string.endswith('Z'):
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    elif '+' in date_string[-6:] or '-' in date_string[-6:]:
        dt = datetime.fromisoformat(date_string)
    else:
        dt = pytz.timezone(from_tz).localize(datetime.fromisoformat(date_string))
    
    return dt.astimezone(pytz.timezone(to_tz))


def analyze_conversation(results):
    summary = {
        "task_id": "",
        # "total_actions": len(results), # TODO: not accurate
        "errored_actions": 0,
        "total_cost": 0,
        "start_timestamp": pytz.timezone('UTC').localize(datetime.now() + timedelta(days=10000)),
        "end_timestamp": pytz.timezone('UTC').localize(datetime.now() - timedelta(days=10000)),
        "runtime_minutes": 0,
    }

    for result in results:
        timestamp = str_to_datetime(result.get("insert_date_"))
        if timestamp:
            summary["start_timestamp"] = min(summary["start_timestamp"], timestamp)
            summary["end_timestamp"] = max(summary["end_timestamp"], timestamp)
        summary["duration_minutes"] = int((summary["end_timestamp"] - summary["start_timestamp"]).total_seconds() / 60)
        if len(result.get("errors", [])) > 0:
            summary["errored_actions"] += 1

        summary["total_cost"] += result.get("cost", 0)

    summary["total_cost"] = round(summary["total_cost"], 1)
    return summary

def clean_metadata(metadata:list):
    cleaned = []
    for i in metadata:
        cleaned.append({i['title']: i['value']})
    return cleaned


if __name__ == "__main__":
    import os
    import json
    from dotenv import load_dotenv
    load_dotenv()

    region_id = os.getenv("region_id")
    project_id = os.getenv("project_id")
    agent_id = os.getenv("agent_id")
    api_key = os.getenv("api_key")

    timezone = "Australia/Sydney"
    from_timestamp = str_to_datetime("2023-01-01", from_tz=timezone, to_tz="UTC")
    to_timestamp = str_to_datetime("2030-01-01", from_tz=timezone, to_tz="UTC")

    response = get_conversations_between_dates(
        region_id,
        project_id,
        agent_id,
        api_key,
        from_timestamp,
        to_timestamp
    )

    full = response.json()
    convos = []
    for convo in full['results']:
        conversation_id = convo['metadata']['_id'].split("_-_")[1]
        studio_results = get_list_conversation_studio_history(region_id, project_id, api_key, agent_id, conversation_id)
        summary = analyze_conversation(studio_results)

        summary['task_id'] = convo.get('knowledge_set', '')
        summary['task_name'] = convo.get('metadata', {}).get('conversation', {}).get('title', '')
        summary['task_state'] = convo.get('metadata', {}).get('conversation', {}).get('state', 'unknown')
        summary['metadata'] = clean_metadata(convo.get('metadata', {}).get('conversation', {}).get('custom_metadata', []))
        convos.append(summary)

    conversation_credits = [convo['total_cost'] for convo in convos]
    aggs = {
        "total_credits": int(sum(conversation_credits)),
        "total_conversations": len(convos),
        "median": round(stats.median(conversation_credits),2),
        "average": round(stats.mean(conversation_credits),2),
        "task_states": Counter(convo['task_state'] for convo in convos)
    }
    print(aggs)
    with open(f'agent_{agent_id}_conversation_costs.json', 'w') as f:
        json.dump(convos, f)

    with open(f'agent_{agent_id}_conversation_costs_summary.json', 'w') as f:
        json.dump(aggs, f)
