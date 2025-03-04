class FilterType:
    EXACT_MATCH = "exact_match"
    EXISTS = "exists"
    REGEXP = "regexp"
    IDS = "ids"
    DATE = "date"
    NUMERIC = "numeric"
    OR = "or"
    AND = "and"
    SIZE = "size"
    ARRAY_OBJECT_MATCH = "array_object_match"

class EventType:
    CONVERSATIONS_CREATED_BY_TRIGGER = "conversations_created_by_trigger"
    CONVERSATIONS_CONTINUED_BY_TRIGGER = "conversations_continued_by_trigger"
    TOOL_RUNS_SUCCEEDED = "tool_runs_succeeded"
    TOOL_RUNS_FAILED = "tool_runs_failed"

class ComparisonType:
    GTE = "gte"
    LTE = "lte"
    BETWEEN = "between"

class ConversationState:
    PAUSED = "paused"
    IDLE = "idle"
    STARTING_UP = "starting-up"
    RUNNING = "running"
    PENDING_APPROVAL = "pending-approval"
    WAITING_FOR_CAPACITY = "waiting-for-capacity"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed-out"
    ESCALATED = "escalated"
    UNRECOVERABLE = "unrecoverable"
    COMPLETED = "completed"
    ERRORED_PENDING_APPROVAL = "errored-pending-approval"
    QUEUED_FOR_APPROVAL = "queued-for-approval"
    QUEUED_FOR_RERUN = "queued-for-rerun"
