from pathlib import Path
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
import openai
import langchain


load_dotenv()
langchain.debug = os.getenv("LANGCHAIN_DEBUG") == "True"


class Config:
    model_name = os.getenv("OPENAI_MODEL")
    llm_cache = os.getenv("LLM_CACHE") == "True"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    assert openai.api_key is not None, "Open AI key not found"
    code_dir = os.getenv("CODE_DIR")
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model_name,
        temperature=0,
        request_timeout=os.getenv("REQUEST_TIMEOUT"),
        cache=llm_cache,
        streaming=True,
        verbose=True,
    )
    ui_timeout = int(os.getenv("REQUEST_TIMEOUT"))
    save_html_path = Path(os.getenv("SAVE_HTML"))

    if not save_html_path.exists():
        save_html_path.mkdir(exist_ok=True, parents=True)

    project_root = Path(os.getenv("PROJECT_ROOT")) / "property_finder"

    size_memory = int(os.getenv("SIZE_MEMORY"))


cfg = Config()


if __name__ == "__main__":
    # print("key: ", cfg.openai_api_key)
    print("model: ", cfg.model_name)
    print("langchain-debug: ", langchain.debug)
