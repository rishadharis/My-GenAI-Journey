# from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
# import os
from langchain import hub
from pathlib import Path
from Tools.tools import get_url_profile_tavily
from streamlit import secrets
import re
from urllib.parse import urlparse


current_dir = Path(__file__).resolve().parent
dotenv_path = current_dir.parent / '.env'

# load_dotenv(dotenv_path)

api_key = secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(
    api_key=api_key,
    model='gpt-4o-mini'
)

def lookup(name: str):
    if is_url(name):
        return name
    template = """
    given the full name {name} I want you to get me a link to their Linkedin profile page. If the url page is given instead of name and the url page is linkedin profile page, then return the url page directly.
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

def is_url(string):
    """
    Check if a string is a valid URL, with or without protocol.
    
    Args:
        string (str): The string to check
        
    Returns:
        bool: True if string is a valid URL, False otherwise
        
    Examples:
        >>> is_url("google.com")
        True
        >>> is_url("https://www.example.com/path?param=value")
        True
        >>> is_url("not-a-url")
        False
    """
    # If no protocol is specified, add https:// for parsing
    if not string.startswith(('http://', 'https://')):
        string = 'https://' + string
    
    try:
        # Basic URL pattern
        url_pattern = re.compile(
            r'^'
            r'(?:http[s]?://)?'  # protocol optional
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip address
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)'  # path
            r'$', re.IGNORECASE)
        
        # Check both regex pattern and urlparse
        result = urlparse(string)
        return bool(url_pattern.match(string) and result.netloc)
    
    except ValueError:
        return False

if __name__ == "__main__":
    linkedin_url = lookup("Rishad Harisdias Bustomi")
    print(linkedin_url)