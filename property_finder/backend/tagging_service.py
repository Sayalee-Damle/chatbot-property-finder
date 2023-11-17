from langchain.chains import LLMChain
from langchain.chains import create_tagging_chain_pydantic
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from property_finder.configuration.config import cfg
from property_finder.configuration.log_factory import logger
from property_finder.backend.model import ResponseTags
from property_finder.configuration.toml_support import read_prompts_toml

prompts = read_prompts_toml()


def prompt_factory_sentiment() -> ChatPromptTemplate:
    section = prompts["tagging_sentiment"]
    human_message = section["human_message"]
    prompt_msgs = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=section["system_message"], input_variables=[]
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message,
                input_variables=["answer"],
            )
        ),
    ]
    return ChatPromptTemplate(messages=prompt_msgs)


def sentiment_chain_factory() -> LLMChain:
    return create_tagging_chain_pydantic(
        ResponseTags, cfg.llm, prompt_factory_sentiment(), verbose=True
    )


###
def prompt_factory_houses() -> ChatPromptTemplate:
    section = prompts["tagging_finding_houses"]
    human_message = section["human_message"]
    prompt_msgs = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=section["system_message"], input_variables=[]
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message,
                input_variables=["text"],
            )
        ),
    ]
    return ChatPromptTemplate(messages=prompt_msgs)


def houses_chain_factory() -> LLMChain:
    return create_tagging_chain_pydantic(
        ResponseTags, cfg.llm, prompt_factory_houses(), verbose=True
    )


def prepare_finding_houses_input(text: str) -> dict:
    return {"text": text}


chain_text = create_tagging_chain_pydantic(
    ResponseTags, cfg.llm, prompt_factory_houses()
)


def tag_response(response: str):
    res = chain_text(prepare_finding_houses_input(response))
    return res


def prompt_factory_memory() -> ChatPromptTemplate:
    section = prompts["memory"]
    human_message = section["human_message"]
    prompt_msgs = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=section["system_message"], input_variables=[]
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message, input_variables=["memory", "question"]
            )
        ),
    ]

    return ChatPromptTemplate(messages=prompt_msgs)


def memory_chain_factory(memory, question) -> LLMChain:
    prompt = prompt_factory_memory()
    chain = LLMChain(llm=cfg.llm, prompt=prompt, verbose=True)
    return chain.run({"memory": memory, "question": question})


chain = create_tagging_chain_pydantic(ResponseTags, cfg.llm, prompt_factory_sentiment())


def prepare_sentiment_input(question: str) -> dict:
    return {"text": question}


def tag_response(response: str):
    res = chain(prepare_sentiment_input(response))
    return res


if __name__ == "__main__":

    def process_answer(answer: str):
        logger.info(type(answer))
        logger.info(answer)

    # Does your organization support an event driven architecture for data integration?

    response_tags: ResponseTags = sentiment_chain_factory().run(
        prepare_sentiment_input("yes")
    )
    process_answer(tag_response(response_tags.is_positive)["answer"])
