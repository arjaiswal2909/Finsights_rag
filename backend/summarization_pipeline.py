from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

def summarize_content(elements):
    chain = (
        {"doc": lambda x: x}
        | ChatPromptTemplate.from_template("Summarize the following tables or text given below:\n\n{doc}")
        | ChatOllama(model="qwen2.5:3b", temperature=0.1)
        | StrOutputParser()
    )
    content = [el.text for el in elements]
    summaries = chain.batch(content, {"max_concurrency": 5})
    return summaries
