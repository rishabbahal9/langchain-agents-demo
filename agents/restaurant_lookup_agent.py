from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from tools.tool import crawls_google


def lookup(
    meal_of_the_day: str, city: str, restaurant_type: str, additional_info: str = ""
) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    prompt_template = PromptTemplate(
        template="""
        Give me a list of 3 to 5 restaurants where I can have {meal_of_the_day}. 
        Make sure the restaurants are in {city}.
        Make sure the restaurants are {restaurant_type}.
        {additional_info}
        """,
        input_variables=[
            "meal_of_the_day",
            "city",
            "restaurant_type",
            "additional_info",
        ],
    )
    tools_for_agent = [
        Tool(
            name="Crawl google for restaurants",
            func=crawls_google,
            description="Useful when you need to find a restaurant in the city",
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
                meal_of_the_day=meal_of_the_day,
                city=city,
                restaurant_type=restaurant_type,
                additional_info=additional_info,
            )
        }
    )

    return result["output"]


if __name__ == "__main__":
    meal_of_the_day_input = input("Enter meal of the day: ")
    city_input = input("Enter city: ")
    restaurant_type_input = input("Enter restaurant type: ")
    additional_info_input = input("Enter information: ")
    lookup(
        meal_of_the_day_input, city_input, restaurant_type_input, additional_info_input
    )
