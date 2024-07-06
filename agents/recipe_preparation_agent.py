from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from tools.tool import crawls_google


def lookup(dish: str, llm_model: str = "gpt-3.5-turbo") -> str:
    llm = ChatOpenAI(temperature=0, model_name=llm_model)
    prompt_template = PromptTemplate(
        template="""
        Give me a list of instructions needed to prepare {dish}. 
        Assume that we are preparing it at home.
        """,
        input_variables=["dish"],
    )
    tools_for_agent = [
        Tool(
            name="Crawl google for instructions to prepare dish",
            func=crawls_google,
            description="Useful when you need to find instructions to prepare a dish",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={
            "input": prompt_template.format_prompt(
                ingredients=ingredients, ethnicity=ethnicity
            )
        }
    )

    return result["output"]


if __name__ == "__main__":
    ingredients_input = input("Enter ingredients: ")
    ethnicity_input = input("Enter your ethnicity: ")
    lookup(ingredients_input, ethnicity_input)
