from property_finder.configuration.log_factory import logger
from property_finder.configuration.config import cfg
from property_finder.backend.tool import agent
import property_finder.backend.tagging_service as ts
from property_finder.backend.model import ResponseTags

def test_find_house_positive():
    assert agent.run("flat with 3 bedrooms"), "Passed"

def test_find_house_negative():
    assert agent.run("flat"), "Failed"

