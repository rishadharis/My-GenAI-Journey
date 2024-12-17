from Package.linkedin import scrape_linkedin_profile
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from Agents.linkedin_lookup_agent import lookup
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    api_key=api_key,
    model='gpt-4o-mini'
)

def get_linkedin_information(name: str) -> str:
    linkedin_url = lookup(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    return linkedin_data

def main():
    information = get_linkedin_information("Rishad Harisdias Bustomi")
    summary_template = """
      Berdasarkan informasi linkedin ini ```{information}``` tentang seseorang, Saya ingin anda membuat 1 paragraf (bukan poin-poin) sarkas (roasting) dengan bahasa jakarta selatan terhadap informasi orang tersebut secara lengkap mulai dan setelahnya tetap diberi yang baik-baiknya seperti "Walaupun begitu.."
    """
    prompt_template = PromptTemplate(
        template=summary_template,
        input_variables=["information"]
    )

    chain = prompt_template | llm
    result = chain.invoke({"information": information})
    print(result.content)

if __name__ == "__main__":
    main()