from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tool import crawls_google


def lookup(ingredients: str, ethnicity: str, llm_model: str = "gpt-3.5-turbo") -> str:
    llm = ChatOpenAI(temperature=0, model_name=llm_model)
    prompt_template = PromptTemplate(
        template="""
        Create a list of 3 recipes which has name of the dish and 1 line description of the dish that I can make using 
        following {ingredients}. 
        Person who wants to eat it is of {ethnicity} origin.
        
        Assume, these are the only ingredients available. You don't need to use all the ingredients.
        """,
        input_variables=["ingredients", "ethnicity"],
    )
    tools_for_agent = [
        Tool(
            name="Crawl google for recipe",
            func=crawls_google,
            description="Useful when you need to find name or names of the recipe/dishes",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

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
