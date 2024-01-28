from enum import Enum


class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class ModelService(str, Enum):
    OPENAI = "openai"


class Model(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    # GPT_4_TURBO = "gpt-4 turbo"


class ResponseFinishReason(str, Enum):
    STOP = "stop"  # complete message, or a message terminated by one of the stop sequences provided via the stop parameter
    LENGTH = "length"  # Incomplete model output due to max_tokens parameter or token limit
    FUNCTION_CALL = "function_call"  # The model decided to call a function
    TOOL_CALLS = "tool_calls"  # The model decided to call a tool
    CONTENT_FILTER = "content_filter"  # Omitted content due to a flag from OpenAI content filters
    NULL = "null"  # API response still in progress or incomplete
