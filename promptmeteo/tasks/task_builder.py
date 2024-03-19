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

from enum import Enum
from typing import Dict, List, Optional

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from ..models import ModelFactory
from ..parsers import ParserFactory
from ..prompts import PromptFactory
from ..selector import SelectorFactory
from .task import Task


class TaskTypes(str, Enum):
    """
    Enum with all the available task types
    """

    QA: str = "qa"
    CLASSIFICATION: str = "classification"
    CODE_GENERATION: str = "code-generation"
    CODE_EXPLAIN: str = "code-explain"
    TITLE: str = "title"
    ADD: str = "add"
    WRITING: str = "writing"
    FIX: str = "fix"
    SCORE: str = "score"
    REVIEW: str = "review"
    ENTITY_RELATIONSHIP: str = "entity-relationship"
    ELEMENT_TYPE: str = "element-type"
    NEXT_ACTION: str = "next-action"
    SUMMARY: str = "summary"
    OUTLINE: str = "outline"
    THOUGHT: str = "thought"
    DIRECTION: str = "direction"
    GOAL: str = "goal"
    GOALSEEK: str = "goalseek"
    REFINEMENT: str = "refinement"
    HEADLINE: str = "headline"
    PREREQUISITE: str = "prerequisite"
    THEME: str = "theme"
    SUB_THEME: str = "sub-theme"
    CONCLUSION: str = "conclusion"
    MILESTONE: str = "milestone"
    TEXT_PLAN: str = "text-plan"
    SENTENCE_PLAN: str = "sentence-plan"
    BEFORE: str = "before"
    AFTER: str = "after"
    COMMON: str = "common"


class TaskBuilder:
    """
    Builder of Tasks.
    """

    def __init__(
        self,
        language: str,
        task_type: str,
        verbose: bool = False,
    ) -> None:
        self._task = Task(
            language=language,
            task_type=task_type,
            verbose=verbose,
        )

    @property
    def task(
        self,
    ) -> Task:
        """Task to built."""
        return self._task

    def build_prompt(
        self,
        model_name: str,
        prompt_order: str,
        prompt_process: str,
        prompt_domain: str,
        prompt_labels: List[str],
        prompt_detail: str,
        prompt_chain_thought: str,
        prompt_answer_format: str,
        prompt_header: str = "",
    ) -> Self:
        """
        Builds a prompt for the task.
        """

        self._task.prompt = PromptFactory.factory_method(
            language=self._task.language,
            task_type=self._task.task_type,
            model_name=model_name,
            prompt_order=prompt_order,
            prompt_process=prompt_process,
            prompt_domain=prompt_domain,
            prompt_labels=prompt_labels,
            prompt_detail=prompt_detail,
            prompt_chain_thought=prompt_chain_thought,
            prompt_answer_format=prompt_answer_format,
            prompt_header=prompt_header,
        )

        return self

    def build_selector_by_train(
        self,
        examples: List[str],
        annotations: List[str],
        selector_k: int,
        selector_type: str,
        selector_algorithm: str,
    ) -> Self:
        """
        Builds a the selector for the task by training a new selector.
        """

        if not self._task.model:
            raise RuntimeError(
                "Selector algorithm is trying yo be built but there is no"
                "LLM model or embeddings loaded. You need to call function"
                "`build_model()` before calling `build_selector()`."
            )

        if not self._task.model.embeddings:
            raise RuntimeError(
                "Selector algorithm is trying yo be built but there is no"
                "embeddigns for model {self._task._model.__name__}."
            )

        embeddings = self._task.model.embeddings

        self._task.selector = SelectorFactory.factory_method(
            language=self._task.language,
            embeddings=embeddings,
            selector_k=selector_k,
            selector_type=selector_type,
            selector_algorithm=selector_algorithm,
        ).train(
            examples=examples,
            annotations=annotations,
        )

        return self

    def build_model(
        self,
        model_name: str = "",
        model_provider_name: str = "",
        model_provider_token: Optional[str] = "",
        model_params: Dict = None,
    ) -> Self:
        """
        Builds a model for the task.
        """

        self._task.model = ModelFactory.factory_method(
            model_name=model_name,
            model_provider_name=model_provider_name,
            model_provider_token=model_provider_token,
            model_params=model_params or {},
        )

        return self

    def build_parser(
        self,
        prompt_labels: List[str],
    ) -> Self:
        """
        Builds a the parser for the task.
        """

        self._task.parser = ParserFactory.factory_method(
            task_type=self._task.task_type,
            prompt_labels=prompt_labels,
        )

        return self

    def build_selector_by_load(
        self,
        model_path: str,
        selector_k: int,
        selector_type: str,
        selector_algorithm: str,
    ) -> Self:
        """
        Builds the selector for the task by loading a pretrained selector.
        """

        if not self._task.model:
            raise RuntimeError(
                "Selector algorithm is trying to be built but there is no"
                "LLM model or embeddings loaded. You need to call function"
                "`build_model()` before calling `load_selector()`."
            )

        if not self._task.model.embeddings:
            raise RuntimeError(
                "Selector algorithm is trying to be built but there is no"
                "embeddigns for model {self._task._model.__name__}."
            )

        embeddings = self._task.model.embeddings

        self._task.selector = SelectorFactory.factory_method(
            language=self._task.language,
            embeddings=embeddings,
            selector_k=selector_k,
            selector_type=selector_type,
            selector_algorithm=selector_algorithm,
        ).load_example_selector(model_path=model_path)

        return self
