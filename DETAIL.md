# PromptMeteo detail

In our use, PromptmeteoProvider are 3 layer(Model, Task, Prompt).
Sequence is here.

1. Model(Base).predict()
2. Task.run()
3. Task._get_prompt()
4. Prompt.run() create INSTRUCTION. -> __LABELS__, __ORDER__,  ...
5. PromptTemplate.from_template() -> __INPUT__, __INSTRUCTION__, __EXAMPLES__
6. Model.run()
7. (omit)Parser.run()
8. Prompt.

## Class

### BaseModel

PromptmeteoProvider/promptmeteo/models/base.py

What LLM is used in Task.

self.llm is langchain BaseLLM.

BaseModel.run() calls llm.predict().

### Task

PromptmeteoProvider/promptmeteo/tasks

Top layer of all.

Task.predict() calls run() of other class(Prompt, ...).

Task.run() is 3 step.

1. \_get_prompt()
2. BaseModel.run()
3. BaseParser.run()

PromptmeteoProvider/promptmeteo/base.py

### Selector

PromptmeteoProvider/promptmeteo/selector

Select by here.

### Prompt

PromptmeteoProvider/promptmeteo/prompts

### BaseParser

PromptmeteoProvider/promptmeteo/parsers/base.py

TODO: read mode code.

### Task

## Prompt structure

PromptmeteoProvider/promptmeteo/tasks/task.py
\_get_prompt()

### **INSTRUCTION**

Prompt.run() create here.

#### **PROMPT_HEADER**

#### **PROMPT_DOMAIN**

#### **PROMPT_DETAIL**

#### **CHAIN_THOUGHT**

#### **ANSWER_FORMAT**

### **EXAMPLES**

Selector class create EXAMPLES.

In no_examples_prompt case, it is empty.

### **INPUT**

PromptmeteoProvider/promptmeteo/base.py

Put example from when Base.predict(examples) is called.(
