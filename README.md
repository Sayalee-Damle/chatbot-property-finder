## Description

This is a chatbot which allows users to search for properties using natural language. This chatbot is based on Langchain Agents and uses the Savills property search engine (https://www.savills.com/).

## Installation instructions


```bash
conda create -n property_finder python=3.11
conda activate property_finder
pip install poetry
# if this doesn't work use : pip install poetry --user
poetry install
```
This creates a specific environment with all the libraries in need!



## To start the chatbot
```chainlit run .\property_finder\frontend\main.py```




## Configuration

To specify configurations use .env file with these keys:

```
OPENAI_API_KEY= openai key
OPENAI_MODEL = gpt-3.5-turbo-16k
CHUNK_SIZE = 1000
TERMINATE_TOKEN =  TERMINATE
REQUEST_TIMEOUT = 300
CODE_DIR = /tmp/property_finder
SAVE_HTML = /tmp/property_finder/html_savills
LLM_CACHE = False
LANGCHAIN_DEBUG = True
PROJECT_ROOT =  the root of your project
SIZE_MEMORY = 5
```
