
from openai import OpenAI
from fastapi import HTTPException, Response

from schemas import Message, BaseModelService
from data_types import Model, ResponseFinishReason, Role
from .message_builder import MessageBuilderOpenAI


class ModelServiceOpenAI(BaseModelService):
    """OpenAI Model Service class"""
    def __init__(self, **kwargs) -> None:
        self.model: Model = kwargs["MODEL"]
        self.feedback_history_length: int = kwargs["FEEDBACK_HISTORY_LENGTH"] if "FEEDBACK_HISTORY_LENGTH" in kwargs else 2
        self.client = OpenAI()
        self.message_builder = MessageBuilderOpenAI()

    def initialize_conversation(self, 
                                initial_message: str,
                                system_message: str = None
                                ) -> list[Message]:
        """Initializes a conversation with the model.
        Returns a list of messages containing the initial model's message and the system message (if provided).

        Args:
            initial_message (str): assistant's (model's) initial message
            system_message (str, optional): initial system message content. Defaults to None.

        Returns:
            list[Message]: list of messages containing the initial model's message and the system message (if provided)
        """
        assistant_message = self.message_builder.get_assistant_message(initial_message)

        if system_message is not None:
            system_message = self.message_builder.get_system_message(system_message)
            messages = [system_message, assistant_message]
        else:
            messages = [assistant_message]

        return messages

    def generate_response(self, messages: list[Message]) -> Message:
        """Generates a response message based on the conversation history.

        Args:
            messages (list[Message]): conversation containing all the history messages

        Returns:
            Message: generated response message
        """
        response = self.send_request(messages)
        content = self.process_response(response)
        message = self.message_builder.get_assistant_message(content)
        return message

    def generate_feedback(self, messages: list[Message], system_message: str = None) -> Message:
        """Generates a feedback message based on the conversation history.

        Args:
            messages (list[Message]): conversation containing all the history messages
            system_message (str, optional): initiali system message content. Defaults to None.

        Returns:
            Message: generated feedback message
        """
        messages = self._process_feedback_input_messages(messages)

        if system_message is not None:
            system_message = self.message_builder.get_system_message(system_message)
            messages = [system_message, *messages[-self.feedback_history_length:]]
        else:
            messages = [*messages[-self.feedback_history_length:]]

        message = self.generate_response(messages)
        return message
    

    def send_request(self, messages: list[Message]) -> Response:
        """Sends a request to the OpenAI API

        Args:
            messages (list[Message]): conversation containing all the history messages

        Returns:
            Response: model service response with the generated message
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response

    def process_response(self, response: Response) -> str:
        """Extracts the generated content message from the model's response

        Args:
            response (Response): model's response

        Returns:
            str: extracted response content
        """
        response_finish_reason = response.choices[0].finish_reason

        if response_finish_reason == ResponseFinishReason.STOP:
            content = response.choices[0].message.content
            return content
        else:
            self._handle_response_finish_reason(response_finish_reason)

    def _handle_response_finish_reason(self, finish_reason: ResponseFinishReason):
        """Handles the reason why the model stopped generating data.

        Args:
            finish_reason (ResponseFinishReason): reason returned by the model

        Raises:
            HTTPException: raised in case of an unknown reason
        """
        if finish_reason == ResponseFinishReason.LENGTH:
            self._handle_max_length_response()
        elif finish_reason == ResponseFinishReason.NULL:
            self._handle_null_response()
        elif finish_reason == ResponseFinishReason.CONTENT_FILTER:
            self._handle_content_filter_response()
        elif finish_reason == ResponseFinishReason.TOOL_CALLS or finish_reason == ResponseFinishReason.FUNCTION_CALL:
            self._handle_tool_calls_response()
        else:
            raise HTTPException(status_code=500, detail="Could not process the request.")

    def _handle_null_response(self):
        # TODO: API response still in progress or incomplete. Wait?
        raise HTTPException(status_code=504, detail="API response still in progress or incomplete.")

    def _handle_max_length_response(self):
        # Idea: summarize conversation?
        raise HTTPException(status_code=409,
                            detail="Sequence too long. The maximum number of tokens specified in the request was reached.")

    def _handle_content_filter_response(self):
        raise HTTPException(status_code=400, detail="Could not process the request as it did not pass the model's content filters.")

    def _handle_tool_calls_response(self):
        raise HTTPException(status_code=400, detail="Request caused the model to use an external tool (function).")

    def _process_feedback_input_messages(self, messages: list[Message]) -> list[Message]:
        # TODO: Refactor
        if len(messages) >= self.feedback_history_length:
            messages = messages[-self.feedback_history_length:]
        else:
            raise HTTPException(status_code=400, detail="Feedback messages must contain at least two messages.")

        for i, message in enumerate(reversed(messages)):
            if message.content is None or len(message.content) == 0:
                raise HTTPException(status_code=400, detail="Feedback messages cannot contain empty messages.")
            if message.role == Role.SYSTEM:
                raise HTTPException(status_code=400, detail="Incorrect conversation history. System messages not allowed.")
            if i % 2 == 0 and message.role != Role.USER:
                raise HTTPException(status_code=400, detail="Incorrect conversation history. User messages must be at even indexes.")
            elif i % 2 != 0 and message.role != Role.ASSISTANT:
                raise HTTPException(status_code=400, detail="Incorrect conversation history. Assistant messages must be at odd indexes.")
        return messages