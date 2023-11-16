from pydantic import Field

from langchain.pydantic_v1 import BaseModel, Field


class ResponseTags(BaseModel):
    """Contains information about the answer given by the user"""

    is_positive: bool = Field(
        ...,
        description="Whether the text with the answers contains a positive tone to it.",
    )
    sounds_confused: bool = Field(
        ...,
        description="Whether the text with the answers suggests that the user is confused.",
    )
    is_negative: bool = Field(
        ...,
        description="Whether the text with the answers contains a negative tone to it.",
    )
    is_correct_output: bool = Field(
        ...,
        description="Whether the text with the answers contains a list of houses in it.",
    )
    is_waste: bool = Field(
        ...,
        description="Whether the text with the answers contains unrelated questions in it.",
    )
