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
from typing import List

import yaml
from langchain.prompts import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate


class BasePrompt(ABC):
    """
    Prompt class interface.
    """

    PROMPT_EXAMPLE = """
        TEMPLATE:
            "Here you explain the task.
            {__PROMPT_ORDER__}
            {__PROMPT_PROCESS__}
            {__PROMPT_DOMAIN__}
            {__PROMPT_LABELS__}

            {__PROMPT_CHAIN_THOUGHT__}
            {__PROMPT_ANSWER_FORMAT__}"

        PROMPT_ORDER:
            "Here you define the {__ORDER__}."
            
        PROMPT_PROCESS:
            "Here you define the {__PROCESS__}."
            
        PROMPT_DOMAIN:
            "Here you explain the {__DOMAIN__} from the texts."

        PROMPT_LABELS:
            "Here you give the {__LABELS__} if required."

        PROMPT_DETAIL:
            "Here you can give some {__DETAIL__}"

        CHAIN_THOUGHT:
            "Explain your answer as {__CHAIN_THOUGHT__}"

        ANSWER_FORMAT:
            "Response as {__ANSWER_FORMAT__}"
            
        PROMPT_HEADER:
            "Prompt header."
    """

    def __init__(
        self,
        prompt_order: str = "",
        prompt_process: str = "",
        prompt_domain: str = "",
        prompt_labels: str = "",
        prompt_detail: str = "",
        prompt_chain_thought: str = "",
        prompt_answer_format: str = "",
        prompt_header: str = "",
    ) -> None:
        """
        Build a Prompt object string given a concrete especification.
        """

        self._prompt_order = prompt_order
        self._prompt_process = prompt_process
        self._prompt_domain = prompt_domain
        self._prompt_labels = prompt_labels
        self._prompt_detail = prompt_detail
        self._prompt_chain_thought = prompt_chain_thought
        self._prompt_answer_format = prompt_answer_format
        self._prompt_header = prompt_header

    @property
    def order(
        self,
    ) -> str:
        """Prompt Order."""
        return self._prompt_order

    @property
    def process(
        self,
    ) -> str:
        """Prompt Process."""
        return self._prompt_process

    @property
    def domain(
        self,
    ) -> str:
        """Prompt Domain."""
        return self._prompt_domain

    @property
    def labels(
        self,
    ) -> List[str]:
        """Prompt Labels."""
        return [self._prompt_labels]

    @property
    def chain_thought(
        self,
    ) -> str:
        """Prompt ChainThought."""
        return self._prompt_chain_thought

    @property
    def answer_format(
        self,
    ) -> str:
        """Prompt AnswerFormat."""
        return self._prompt_answer_format

    @property
    def template(
        self,
    ) -> str:
        """Prompt Template."""
        return self.run().format()

    @classmethod
    def read_prompt(
        cls,
        prompt_text: str,
    ) -> None:
        """
        Reads a Promptmeteo prompt string to build the Task Prompt. Promptmeteo
        prompts are expected to follow the following template:


        Parameters
        ----------

        prompt_text : str


        Returns
        -------

        Self

        """

        try:
            prompt = yaml.load(prompt_text, Loader=yaml.FullLoader)

        except Exception as error:
            raise ValueError(
                f"`{cls.__name__}` error in function `read_prompt()`. "
                f"The expected string input should be like:\n\n"
                f"{cls.PROMPT_EXAMPLE}\n\n{error}"
            ) from error

        try:
            cls.TEMPLATE = prompt.get("TEMPLATE", "")
            cls.PROMPT_ORDER = prompt.get("PROMPT_ORDER", "")
            cls.PROMPT_PROCESS = prompt.get("PROMPT_PROCESS", "")
            cls.PROMPT_DOMAIN = prompt.get("PROMPT_DOMAIN", "")
            cls.PROMPT_LABELS = prompt.get("PROMPT_LABELS", "")
            cls.PROMPT_DETAIL = prompt.get("PROMPT_DETAIL", "")
            cls.PROMPT_ANSWER_FORMAT = prompt.get("PROMPT_ANSWER_FORMAT", "")
            cls.PROMPT_CHAIN_THOUGHT = prompt.get("PROMPT_CHAIN_THOUGHT", "")
            cls.ANSWER_FORMAT = prompt.get(
                "ANSWER_FORMAT", ""
            )  # direct fix str in template
            cls.CHAIN_THOUGHT = prompt.get(
                "CHAIN_THOUGHT", ""
            )  # direct fix str in template
            cls.PROMPT_HEADER = prompt.get("PROMPT_HEADER", "")

            cls.PROMPT_EXAMPLE = prompt_text

        except Exception as error:
            raise ValueError(
                f"`{cls.__name__}` error `read_prompt()`. The expected keys "
                f"are {yaml.load(cls.PROMPT_EXAMPLE, Loader=yaml.FullLoader)}"
            ) from error

    def run(
        self,
    ) -> PromptTemplate:
        """
        Returns the prompt template for the current task.
        """

        def format_variable(value):
            return "\n - ".join([""] + value) if isinstance(value, list) else value

        def format_prompt(template, variables):
            formatted_variables = {
                k: format_variable(v) for k, v in variables.items() if v
            }
            try:
                return template.format(**formatted_variables) if template else ""
            except KeyError:
                return ""

        # Variables
        variables = {
            "__LABELS__": self._prompt_labels,
            "__ORDER__": self._prompt_order,
            "__PROCESS__": self._prompt_process,
            "__DOMAIN__": self._prompt_domain,
            "__DETAIL__": self._prompt_detail,
            "__ANSWER_FORMAT__": self._prompt_answer_format,
            "__CHAIN_THOUGHT__": self._prompt_chain_thought,
            "__HEADER__": self._prompt_header,
        }

        # Prompts
        prompts = {
            "labels": self.PROMPT_LABELS,
            "order": self.PROMPT_ORDER,
            "process": self.PROMPT_PROCESS,
            "domain": self.PROMPT_DOMAIN,
            "detail": self.PROMPT_DETAIL,
            "answer_format": self.PROMPT_ANSWER_FORMAT,
            "chain_thought": self.PROMPT_CHAIN_THOUGHT,
            "header": self.PROMPT_HEADER,
        }

        pipeline_prompts = [
            (
                f"__PROMPT_{k.upper()}__",
                PromptTemplate.from_template(format_prompt(v, variables)),
            )
            for k, v in prompts.items()
        ]
        # Add __ANSWER_FORMAT__ and __CHAIN_THOUGHT__ to pipeline_prompts
        pipeline_prompts.extend(
            [
                (
                    "__ANSWER_FORMAT__",
                    PromptTemplate.from_template(
                        format_prompt(self.ANSWER_FORMAT, variables)
                    ),
                ),
                (
                    "__CHAIN_THOUGHT__",
                    PromptTemplate.from_template(
                        format_prompt(self.CHAIN_THOUGHT, variables)
                    ),
                ),
            ]
        )

        return PipelinePromptTemplate(
            final_prompt=PromptTemplate.from_template(self.TEMPLATE),
            pipeline_prompts=pipeline_prompts,
        )
