import os, getpass
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from helpers import get_system_prompt

load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("GROQ_API_KEY")

llm = ChatGroq(
    model=os.environ.get("LLM_MODEL", "llama-3.3-70b-versatile"), 
    temperature=0.3,
    max_tokens=5000,
    api_key=os.environ.get("GROQ_API_KEY")
)

system_prompt = get_system_prompt()

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

parser = StrOutputParser()

mem = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

def chain_with_mem():
    def get_chat_history():
        return mem.chat_memory.messages
    
    return (
        {
            "question": RunnablePassthrough(),
            "chat_history": lambda x: get_chat_history()
        }
        | agent_prompt
        | llm
        | parser
    )

chain = chain_with_mem()

try:
    response = chain.invoke("Hello my agent")
    mem.save_context({"question": "Hello my agent"}, {"output": response})
    print(response)

    while True:
        instruction = input("")
        response = chain.invoke(instruction)
        print(f"Agent: {response}")

except KeyboardInterrupt:
    print("Kwaheri")