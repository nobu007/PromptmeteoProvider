import os
import sys
from enum import Enum
from typing import Dict, Optional

from langchain.embeddings import VertexAIEmbeddings
from langchain.llms import VertexAI

from .base import BaseModel

# commonモジュールをインポートする
COMMON_MOD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../common"))
sys.path.append(COMMON_MOD_DIR)

LIB_DECORATOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "lib/document_decorator"))
sys.path.append(LIB_DECORATOR_DIR)

from yka_langchain import yka_langchain_raw


class ModelTypes(str, Enum):
    """
    Enum of available model types.
    """

    YkaCodeGen: str = "yka-llm_code-gen"
    YkaCodeExplain: str = "yka-llm"
    YkaDocument: str = "yka-llm_document"

    # TextDavinci003: str = "text-davinci-003"

    @classmethod
    def has_value(
        cls,
        value: str,
    ) -> bool:
        """
        Checks if the value is in the enum or not.
        """

        return value in cls._value2member_map_


class ModelParams(Enum):
    """
    Model Parameters.
    """

    class YkaCodeGen:
        """
        Default parameters for code-generation model.
        """

        model_task: str = "code-generation"
        model_kwargs = {"temperature": 0.4, "max_tokens": 256, "max_retries": 3}

    class YkaCodeExplain:
        """
        Default parameters for code-explain model.
        """

        model_task: str = "code-explain"
        model_kwargs = {"temperature": 0.4, "max_tokens": 256, "max_retries": 3}

    class YkaDocument:
        """
        Default parameters for code-explain model.
        """

        model_task: str = "document-add"
        model_kwargs = {"temperature": 0.4, "max_tokens": 256, "max_retries": 3}


class YkaLLM(BaseModel):
    """
    Yka LLM model wrapper.
    """

    def __init__(
        self,
        model_name: Optional[str] = "",
        model_params: Optional[Dict] = None,
        model_provider_token: Optional[str] = "",
        model_provider_project: Optional[str] = None,
    ) -> None:
        """
        Make predictions using a Yka llm model wrapper.
        """

        if not ModelTypes.has_value(model_name):
            raise ValueError(
                f"`model_name`={model_name} not in supported model names: " f"{[i.name for i in ModelTypes]}"
            )
        super(YkaLLM, self).__init__()

        self._llm = None  # llm is set inner Yka function.

        self._embeddings = None  # VertexAIEmbeddings()

        if not model_params:
            model_params = ModelParams[ModelTypes(model_name).name].value
        self.model_params = model_params

    def run(
        self,
        sample: str,
        is_smart: bool = False,
    ) -> str:
        """
        Executes the model LLM and return its prediction.
        """

        try:
            messages = [{"role": "user", "content": str(sample)}]
            response = yka_langchain_raw(messages=messages, is_smart=is_smart)
            return response

        except Exception as error:
            print(error)
            raise error
            # raise RuntimeError(
            #     f'Error generating from LLM: with sample "{sample}"'
            # ) from error
