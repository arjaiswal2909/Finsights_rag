from langchain_core.output_parsers import StrOutputParser
from langchain.llms import Ollama
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

def run_rag_pipeline(query, retriever):
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based only on the following context, which can include text and tables:{context}\n\nQuestion: {question}"
    )
    model = Ollama(model="qwen2.5:3b", temperature=0)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)