import getpass, os
from dotenv import load_dotenv

load_dotenv()

required_api_keys={
    "GROQ_API_KEY": "Enter groq API Key: ", 
    "CANVAS_API_BASEURL": "Enter CANVAS Instance URL: ", 
    "CANVAS_LMS_API_TOKEN": "Enter CANVAS LMS token: "
}

for keyname, description in required_api_keys.items():
    if not os.environ.get(keyname):
        os.environ[keyname] = getpass.getpass(description)


from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.output_parsers import StructuredOutputParser
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from utils.tools import all_courses, all_course_students, student_progress

llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.3,
    max_tokens=500
)

system_prompt = f"""
You are a Canvas LMS Assistant. You help instructors monitor students progress
and provide actionable, personalized recommendations based on Canvas LMS data for these courses.
{all_courses}

Use provide tools to:-
- get course information 
- retrieve students grades, progress, assignment submissions rate
- use the information to construct a comprehesive report about a student

When responding, provide clear specific insights for struggling students.
Use the students perfomance data to formulate suggestions for improvements or pair programming partner
You are capable of constructing follow up emails to students who are lagging behind.

Do not call the tool for all courses and all students, just for the provided course or student id
"""

tools = [
    all_courses, 
    all_course_students, 
    student_progress
]

agent_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    HumanMessage(content="{instruction}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("How can I help you today? \n")
while True:
    instruction = input("")
    response = agent_executor.invoke({
        "instruction": instruction
    })

    print(response["output"])