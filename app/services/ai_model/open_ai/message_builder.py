from schemas import Message
from data_types import Role


class MessageBuilderOpenAI:
    """Message Builder class for OpenAI API Model Service.
    
    - `system` - a message which gives the context of a conversation. It helps set the behavior of the assistant.
    - `assistant` - the chatbot itself
    - `user` - the actual user
    """
    def __init__(self, default_message: str = None) -> None:
        self.default_message = default_message

    def get_system_message(self, content: str) -> Message:
        """Returns a system message.

        Args:
            content (str): content of the message

        Returns:
            Message: built system message
        """
        return Message(role=Role.SYSTEM, content=content)

    def get_assistant_message(self, content: str) -> Message:
        """Returns an assistant message.

        Args:
            content (str): content of the message

        Returns:
            Message: built assistant message
        """
        return Message(role=Role.ASSISTANT, content=content)

    def get_user_message(self, content: str) -> Message:
        """Returns a user message.

        Args:
            content (str): content of the message

        Returns:
            Message: built user message
        """
        return Message(role=Role.USER, content=content)
