from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from.env file

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# llm = ChatOpenAI(api_key=api_key, temperature=0, model_name="gpt-4o-mini")
llm = ChatAnthropic(api_key=anthropic_api_key, temperature=0, model_name="claude-3-5-haiku-20241022")

information = """
Elon Reeve Musk FRS (/ˈiːlɒn/; born June 28, 1971) is a businessman known for his key roles in the space company SpaceX and the automotive company Tesla, Inc. His other involvements include ownership of X Corp., the company that operates the social media platform X (formerly Twitter), and his role in the founding of the Boring Company, xAI, Neuralink, and OpenAI. Musk is the wealthiest individual in the world; as of December 2024, Forbes estimates his net worth to be US$432 billion.[2]

A member of the wealthy South African Musk family, Musk was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at the age of 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but never enrolled in classes, and with his brother Kimbal co-founded the online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999. That same year, Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal. In 2002, Musk acquired US citizenship, and that October eBay acquired PayPal for $1.5 billion. Using $100 million of the money he made from the sale of PayPal, Musk founded SpaceX, a spaceflight services company, in 2002.

In 2004, Musk was an early investor in electric-vehicle manufacturer Tesla Motors, Inc. (later Tesla, Inc.), providing most of the initial financing and assuming the position of the company's chairman. He later became the product architect and, in 2008, the CEO. In 2006, Musk helped create SolarCity, a solar energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, he proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year Musk co-founded Neuralink, a neurotechnology company developing brain–computer interfaces, and The Boring Company, a tunnel construction company. In 2018 the U.S. Securities and Exchange Commission (SEC) sued Musk, alleging that he had falsely announced that he had secured funding for a private takeover of Tesla. To settle the case Musk stepped down as the chairman of Tesla and paid a $20 million fine. In 2022, he acquired Twitter for $44 billion, merged the company into the newly-created X Corp. and rebranded the service as X the following year. In March 2023, Musk founded xAI, an artificial-intelligence company.
"""

def main():
    summary_template = """
      Given the information ```{information}``` about a person, I want you to create:
      1. a short summary
      2. two interesting facts about them
    """
    prompt_template = PromptTemplate(
        template=summary_template,
        input_variables=["sentence","language"]
    )

    chain = prompt_template | llm
    result = chain.invoke({"information": information})
    print(result.content)

if __name__ == "__main__":
    main()