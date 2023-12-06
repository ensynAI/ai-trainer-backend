from fastapi import HTTPException
from data_types import ResponseFinishReason


def handle_response_finish_reason(finish_reason: ResponseFinishReason):
    if finish_reason == ResponseFinishReason.LENGTH:
        handle_max_length_response()
    elif finish_reason == ResponseFinishReason.NULL:
        handle_null_response()
    elif finish_reason == ResponseFinishReason.CONTENT_FILTER:
        handle_content_filter_response()
    elif finish_reason == ResponseFinishReason.TOOL_CALLS or finish_reason == ResponseFinishReason.FUNCTION_CALL:
        handle_tool_calls_response()
    else:
        raise HTTPException(status_code=500, detail="Could not process the request.")


def handle_null_response():
    # TODO: API response still in progress or incomplete. Wait?
    raise HTTPException(status_code=504, detail="API response still in progress or incomplete.")


def handle_max_length_response():
    # Idea: summarize conversation?
    raise HTTPException(status_code=409,
                        detail="Sequence too long. The maximum number of tokens specified in the request was reached.")


def handle_content_filter_response():
    raise HTTPException(status_code=400, detail="Could not process the request as it did not pass the model's content filters.")


def handle_tool_calls_response():
    raise HTTPException(status_code=400, detail="Request caused the model to use an external tool (function).")
