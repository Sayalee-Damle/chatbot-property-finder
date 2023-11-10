import chainlit as cl

from property_finder.configuration.log_factory import logger
from property_finder.configuration.config import cfg
from property_finder.backend.tool import agent
import property_finder.backend.tagging_service as ts
from property_finder.backend.model import ResponseTags


def answer(input_msg: str):
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
        return "did not understand"

async def ask_user_msg(question):
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(
            content=f"{question}", timeout=cfg.ui_timeout, raise_on_timeout= True
        ).send()
    return ans

@cl.on_chat_start
async def start() -> cl.Message:
    await cl.Message(content="Welcome To The Property Finder, You can find properties in London and India").send()
    await cl.Message(content="You need to specify \"London\" if you want a house there").send()
    requirements = await ask_user_msg("What are the requirements for your house?")
    requirements_list = requirements['content']
    while True:
        #logger.info(requirements['content'])
        list_of_houses = await cl.make_async(agent.run)(requirements_list)
        await cl.Message(content=list_of_houses).send()

        requirements_more = await ask_user_msg("What else can you describe?")
        if answer(requirements_more['content']) == "negative":
            await cl.Message(content="Thank You!").send()
            break
            
        requirements_list = requirements_more['content']
        
        