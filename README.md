## Description

This tool uses autogen to create agents. It accesses a LinkedIn page and gives the summary of the page.

## Installation instructions


```
conda create -n property_finder python=3.11
conda activate property_finder
pip install poetry
poetry install
```
This creates a specific environment with all the libraries in need!



## to start the chatbot
```chainlit run .\property_finder\frontend\main.py```




## Configuration
configure the .env file might like this:
To specify configurations use .env file

```
OPENAI_API_KEY= openai key
OPENAI_MODEL = gpt-3.5-turbo-16k
CHUNK_SIZE = 1000
TERMINATE_TOKEN =  TERMINATE
REQUEST_TIMEOUT = 300
SEED = 42
TEMPERATURE = 0
MAX_AUTO_REPLY = 4
CODE_DIR = /tmp/property_finder
SAVE_HTML = /tmp/property_finder/html_savills
LLM_CACHE = False
LANGCHAIN_DEBUG = True
PROJECT_ROOT =  the root of your project
```
