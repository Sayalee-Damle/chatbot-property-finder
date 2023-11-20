import chainlit as cl

from property_finder.configuration.log_factory import logger
from property_finder.configuration.config import cfg
from property_finder.backend.tool import agent
import property_finder.backend.tagging_service as ts
from property_finder.backend.model import ResponseTags
from property_finder.backend.memory import memory


async def answer(input_msg: str):
    response_tags: ResponseTags = ts.sentiment_chain_factory().run(
        ts.prepare_sentiment_input(input_msg)
    )
    logger.info(response_tags)
    if response_tags.is_positive:
        return "positive"
    elif response_tags.is_negative:
        return "negative"
    elif response_tags.sounds_confused:
        return "confused"
    else:
        return "I can't understand"


async def correct_output_finder(input_msg: str):
    response_tags: ResponseTags = ts.houses_chain_factory().run(
        ts.prepare_finding_houses_input(input_msg)
    )
    logger.info(response_tags)
    if response_tags.is_correct_output:
        return "correct"
    elif response_tags.is_waste:
        return "doesn't relate"
    elif response_tags.sounds_confused:
        return "confused"
    else:
        return "I can't understand"


async def memory_save(requirements_list: str, question: str):
    logger.info("in memory")
    memory.memory_list.append(requirements_list)
    if len(memory.memory_list) == cfg.size_memory:
        memory.memory_list.pop(0)
    memory_string = " ".join(memory.memory_list)
    return ts.memory_chain_factory(memory_string, question)


async def ask_user_msg(question):
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(
            content=f"{question}", timeout=cfg.ui_timeout, raise_on_timeout=True
        ).send()
    return ans


@cl.on_chat_start
async def start() -> cl.Message:
    await cl.Message(
        content="Welcome To The Property Finder, You can find properties in London and India"
    ).send()

    initial_ques = "What are the requirements for your house?"
    while True:
        requirements = await ask_user_msg(initial_ques)
        requirements_list = requirements["content"]

        val = await memory_save(requirements_list, initial_ques)
        list_of_houses = await get_list_houses(requirements_list, val)
        type_answer = await correct_output_finder(list_of_houses)
        logger.info(type_answer)
        if type_answer == "confused":
            initial_ques = "What else can you describe?"
            requirements = await ask_user_msg(initial_ques)
            val = await memory_save(requirements["content"], initial_ques)
            # list_of_houses = await get_list_houses(requirements_list, val)

        elif type_answer == "correct":
            initial_ques = "We can find more properties with different specifications, please enter the specifications"
            memory.memory_list = []
            continue

        else:
            initial_ques = "Can you please tell me the requirements for your house so that I can find one for you?"
            memory.memory_list = []
            continue
        # requirements_list = requirements['content']


async def get_list_houses(requirements_list, val):
    content_requirements = requirements_list + " " + val
    list_of_houses = await cl.make_async(agent.run)(content_requirements)
    await cl.Message(content=list_of_houses).send()
    return list_of_houses


if __name__ == "__main__":
    logger.info(memory.memory_list)
