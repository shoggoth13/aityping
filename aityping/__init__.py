from langchain.chains.openai_functions import (
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel, Field


class ValidationResponse(BaseModel):
    reasoning: str = Field(
        description="Thought process for whether or not the user input is valid."
    )
    is_valid: bool = Field(
        description="Whether or not the user input is valid according to conditions."
    )


class ShortValidationResponse(BaseModel):
    is_valid: bool = Field(
        description="Whether or not the user input is valid according to conditions."
    )


prompt_msgs = [
    SystemMessagePromptTemplate.from_template(
        "You need to whether a user's input satisfies the following conditions:\n\n{conditions}"
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
]
default_prompt = ChatPromptTemplate(messages=prompt_msgs)


def get_ai_type(condition: str, include_reasoning=False, llm=None):
    _type = ValidationResponse if include_reasoning else ShortValidationResponse
    llm = llm or ChatOpenAI(temperature=0)
    chain = create_structured_output_chain(_type, llm, default_prompt)

    class AIMeta(type):
        def __instancecheck__(cls, instance):
            if instance is None:
                return False
            check = chain.run(conditions=condition, input=instance)
            return check.is_valid

    class AIType(metaclass=AIMeta):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v):
            if v is None:
                return False
            check = chain.run(conditions=condition, input=v)
            if not check.is_valid:
                if isinstance(check, ValidationResponse):
                    raise TypeError(check.reasoning)
                else:
                    raise TypeError("Flagged as invalid.")
            return v

    return AIType
