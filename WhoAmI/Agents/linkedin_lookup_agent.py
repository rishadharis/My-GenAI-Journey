from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
import os
from langchain import hub
from pathlib import Path
from Tools.tools import get_url_profile_tavily


current_dir = Path(__file__).resolve().parent
dotenv_path = current_dir.parent / '.env'

load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    api_key=api_key,
    model='gpt-4o-mini'
)

def lookup(name: str):
    template = """
    given the full name {name} I want you to get me a link to their Linkedin profile page.
    Your answer should only contain only a URL
    """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn Profile Page",
            func=get_url_profile_tavily,
            description="useful for when you need to get a LinkedIn profile page",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        {"input": prompt_template.format_prompt(name=name)}
    )
    linkedin_profile_url = result["output"]

    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup("Rishad Harisdias Bustomi")
    print(linkedin_url)