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
from typing import List

from .base import BaseParser
from .classification_parser import ClassificationParser
from .dummy_parser import DummyParser


class ParserTypes(str, Enum):
    """
    Enum of availables parsers.
    """

    PARSER_1: str = "classification"
    PARSER_2: str = "ner"
    PARSER_3: str = "qa"
    PARSER_4: str = "code-generation"
    PARSER_5: str = "code-explain"
    PARSER_6: str = "title"
    PARSER_7: str = "add"
    PARSER_8: str = "writing"
    PARSER_9: str = "fix"
    PARSER_10: str = "score"
    PARSER_11: str = "review"
    PARSER_12: str = "entity-relationship"
    PARSER_13: str = "element-type"
    PARSER_14: str = "next-action"
    PARSER_15: str = "summary"
    PARSER_16: str = "outline"
    PARSER_17: str = "theme"
    PARSER_18: str = "direction"
    PARSER_19: str = "thought"
    PARSER_20: str = "goal"
    PARSER_21: str = "goalseek"
    PARSER_22: str = "refinement"
    PARSER_23: str = "headline"


class ParserFactory:
    """
    Factory of Parsers.
    """

    @classmethod
    def factory_method(
        cls,
        task_type: str,
        prompt_labels: List[str],
    ):
        """
        Returns and instance of a BaseParser object depending on the
        `task_type`.
        """

        if task_type == ParserTypes.PARSER_1.value:
            parser_cls = ClassificationParser

        elif task_type in [parser_type.value for parser_type in ParserTypes]:
            parser_cls = DummyParser

        else:
            raise ValueError(
                f"`{cls.__name__}` error in function `factory_method()`: "
                f"{task_type} is not in the list of supported providers: "
                f"{[i.value for i in ParserTypes]}"
            )

        return parser_cls(
            prompt_labels=prompt_labels,
        )
