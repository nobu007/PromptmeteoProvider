# PromptMeteo detail

In our use, PromptmeteoProvider run 3 layer.

1. Task.
2. Model.
3. Prompt.


## Class

### Task

PromptmeteoProvider/promptmeteo/tasks

Top layer of all.

Task.predict() calls run() of other class(Prompt, ...).

Task.run() is 3 step.

1. _get_prompt()
2. BaseModel.run()
3. BaseParser.run()


### BaseModel

PromptmeteoProvider/promptmeteo/models/base.py

What LLM is used in Task.


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
