from abc import ABC, abstractmethod


class LLMBaseModel(ABC):

    @abstractmethod
    def invoke(
        self,
        model: str,
        contents: list[str]
    ) -> str:
        """
        Invoke the LLM model with the given contents.
        """
        pass

    @abstractmethod
    def get_token_info(self, text: str) -> int:
        """
        Get the number of tokens in the given text.
        """
        pass

    @abstractmethod
    def invoke_stream(
        self,
        model: str,
        contents: list[str]
    ) -> str:
        """
        Invoke the LLM model with the given text and return a stream of responses.
        """
        pass
