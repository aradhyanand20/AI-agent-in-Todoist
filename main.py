from dotenv import load_dotenv
import os
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor

load_dotenv()

todoist_api_key = os.getenv("TODOIST_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

@tool
def add_task():
    """
   Add a new task to the user's task list. Use this when the user  wants to add or create a task """
    print("adding a task")
    print("task added")

tools = [add_task]

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash', 
    google_api_key=gemini_api_key,
     temperature=0.3)

system_propmt = "You are a helpful assistant. You will help with the user and tasks"                 
user_input = "Add task to buy some milk"

prompt = ChatPromptTemplate.from_messages([
    ("system", system_propmt),
    ("human", user_input),
    MessagesPlaceholder("agent_scratchpad")  # type: ignore
])
agent = create_openai_functions_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent,tools = tools,verbose=True)

response = agent_executor.invoke({"input": user_input})

print(response['output'])
# chain =prompt | llm | StrOutputParser()
# print(chain)
# response = chain.invoke({"input": user_input})
# print(response)