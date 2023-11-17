system_message = "You are an expert in extracting informtaion"

human_message = """
You will be given a message: {user_input}, please extract the following attributes
1. property type
2. minimum number of bedrooms
return result in a JSON format, with key value pairs.
Please give the result only after this sentence 'the result in JSON format would be:'
"""

system_message_read_data = "you are an expert data interpreter"

human_message_read_data = """
you will be given data from a text file. You have to find the properties present in {data} and list them down.
"""
system_message_data_capture = "You are an expert in capturing data from markdown"
human_message_data_capture = """
You will be given a markdown file {file}, capture the data and the way the data is written. Give a good structured output.
"""
