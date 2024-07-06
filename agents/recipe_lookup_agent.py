from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from output_parsers import recipe_name_data_parser
from tools.tool import crawls_google


def lookup(ingredients: str, ethnicity: str, llm_model: str = "gpt-3.5-turbo") -> str:
    llm = ChatOpenAI(temperature=0, model_name=llm_model)
    prompt_template = PromptTemplate(
        template="""
        Give me a name and 1 line description of the 1 dish that I can make using following {ingredients}. 
        Person who wants to eat it is of {ethnicity} origin.
        
        Assume, these are the only ingredients available. You don't need to use all the ingredients.
        """,
        input_variables=["ingredients", "ethnicity"],
    )
    tools_for_agent = [
        Tool(
            name="Crawl google for recipe",
            func=crawls_google,
            description="Useful when you need to find name of the recipe/dishes",
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

    return result["output"] | recipe_name_data_parser


if __name__ == "__main__":
    ingredients_input = input("Enter ingredients: ")
    ethnicity_input = input("Enter your ethnicity: ")
    lookup(ingredients_input, ethnicity_input)
