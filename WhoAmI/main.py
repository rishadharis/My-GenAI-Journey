from Package.linkedin import scrape_linkedin_profile
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# llm = ChatOpenAI(api_key=api_key, temperature=0, model_name="gpt-4o-mini")
llm = ChatAnthropic(api_key=anthropic_api_key, temperature=0, model_name="claude-3-5-haiku-20241022")

def main():
    information = scrape_linkedin_profile(mock=True)
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