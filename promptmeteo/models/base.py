#!/usr/bin/python3

#  Copyright (c) 2023 Paradigma Digital S.L.

#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from abc import ABC
from langchain.llms.base import BaseLLM
from langchain.embeddings.base import Embeddings


class BaseModel(ABC):
    """
    Model Interface.
    """

    def __init__(self):
        self._llm: BaseLLM = None
        self._embeddings: Embeddings = None

    @property
    def llm(
        self,
    ) -> BaseLLM:
        """Get Model LLM."""
        return self._llm

    @property
    def embeddings(
        self,
    ) -> Embeddings:
        """Get Model Embeddings."""
        return self._embeddings

    def run(
        self,
        sample: str,
        is_smart: bool = False,
    ) -> str:
        """
        Executes the model LLM and return its prediction.
        """

        try:
            return self._llm(prompt=sample, is_smart=is_smart)

        except Exception as error:
            raise RuntimeError(
                f'Error generating from LLM: with sample "{sample}"'
            ) from error
