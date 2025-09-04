from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from helpers import get_system_prompt

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0.3,
    max_tokens=5000
)

system_prompt = get_system_prompt()

agent_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessage(content="{instruction}")
])

parser = StrOutputParser()

mem = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

def chain_with_mem():
    def get_chat_history():
        return mem.chat_memory.messages
    
    return (
        {
            "instruction": RunnablePassthrough(),
            "chat_history": lambda x: get_chat_history()
        }
        | agent_prompt
        | llm
        | parser
    )

chain = chain_with_mem()


response = chain.invoke({"instruction": "Hello my agent"})
mem.save_context({"instruction": "Hello my agent"}, {"output": response})
print(response)

try:
    while True:
        instruction = input("")
        print(instruction)
        response = chain.invoke({
            "instruction": instruction
        })

        print(f"Agent: {response}")
        print("""
    Awaiting next instructions: -
    """)
except KeyboardInterrupt:
    print("Kwaheri")