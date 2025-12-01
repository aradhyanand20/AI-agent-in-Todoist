from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from todoist_api_python.api import TodoistAPI

load_dotenv()

todoist_api_key = os.getenv("TODOIST_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
todoist = TodoistAPI(todoist_api_key)


@tool
def add_task(task,desc):
    """
   Add a new task to the user's task list. Use this when the user  wants to add or create a task """
    todoist.add_task(content=task,
                     description=desc)
    
@tool
def show_task():
    """
    show all the existing task to the user
    """
    result_paginator = todoist.get_tasks()
    tasks = []
    for tasklist in result_paginator:
        for task in tasklist:
            tasks.append(task.content)
    return tasks
            
<<<<<<< HEAD
    #  tools list
=======
    
>>>>>>> 21677b499b1047778f463f0669bf7a86aaa13e1d
tools = [add_task, show_task]

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash', 
    google_api_key=gemini_api_key,
     temperature=0.3)

system_propmt = "You are a helpful assistant. You will help with the user  add tasks.You will help the user to show existing tasks if user ask to show the tasks: for example: 'show me the task' similar to it  and also print them in bullet list format. If the question is not a tool-related question then answer normally"                 

prompt = ChatPromptTemplate.from_messages([
    ("system", system_propmt),
    MessagesPlaceholder("history"),
    ("user", "{input}"),
    MessagesPlaceholder("agent_scratchpad")  # type: ignore
])
agent = create_openai_functions_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent,tools = tools,verbose=False)

history = []
while True:
    user_input = input("you: ")
    response = agent_executor.invoke({"input": user_input, "history":history})
    print(response['output'])
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response["output"]))




# chain =prompt | llm | StrOutputParser()
# print(chain)
# response = chain.invoke({"input": user_input})
# print(response)