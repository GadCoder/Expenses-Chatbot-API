from abc import ABC, abstractmethod


class BaseLLMService(ABC):
    @abstractmethod
    def get_function_call(self, prompt: str) -> tuple | None:
        """
        Get a function call from the LLM service.
        """
        pass
