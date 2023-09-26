from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from system_messages import system_messages
import pickle
import os
os.environ["OPENAI_API_KEY"] = ""
name = os.environ.get('author')
books = f"books/{name}.txt"

with open(f"vectordbs/{name}.pkl", "rb") as f:
    db = pickle.load(f)

llm = ChatOpenAI(temperature=0.9)

def change_format(history):
    history_f = []
    for i in history:
        role = "human" if i["role"] == "user" else "ai"
        content = i["content"]
        history_f.append((role, content))
    return history_f

def ask(question, history):
    # 
    history.append({"role": "user", "content": question})
    # 改变格式
    history_f = change_format(history)
    # 向量数据库搜索
    text = db.similarity_search(question)
    template = ChatPromptTemplate.from_messages([
        ("system", system_messages[name]),
        *history_f
    ])
    # 
    messages = template.format_messages(
        text=text,
    )
    # 请求
    answer = llm(messages).content
    #
    history.append({"role": "assistant", "content": answer})
    #
    messages = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]

    return messages, history

if __name__ == "__main__":
    print(ask("How to reach communism"))
