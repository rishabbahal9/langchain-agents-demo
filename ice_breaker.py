from langchain.prompts.prompt import Prompt, PromptTemplate
from langchain_openai import ChatOpenAI
from agents.recipe_lookup_agent import lookup as recipe_lookup_agent
from chains.custom_chains import CustomChains

from output_parsers import RecipesNameData


class Cooking:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        print(f"Using model: {self.model}")

    @staticmethod
    def check():
        print("Hello, Langchain!")

    def recipe_generator(self):
        """A simple LLM call"""
        ingredients = input("Enter ingredients: ")
        template = PromptTemplate(
            template="""Give me a list of 5 recipes that I can make using {ingredient}.""",
            input_variables=["ingredient"],
        )
        llm = ChatOpenAI(
            temperature=0,
            model_name=self.model,
        )
        chain = template | llm

        return chain.invoke(input={"ingredient": ingredients})

    def recipe_generator_agent(self):
        """Generating recipes using an agent with web tool"""
        ingredients = input("Enter ingredients: ")
        ethnicity = input("Enter ethnicity/cuisine: ")

        # Gives a list of names of 5 recipes/dishes
        recipe_response = recipe_lookup_agent(ingredients, ethnicity, self.model)

        dishes_chain = CustomChains(self.model).get_dish_chain()
        parsed_response: RecipesNameData = dishes_chain.invoke(
            input={"recipe_list_data": recipe_response}
        )

        return parsed_response


if __name__ == "__main__":
    # Calling static method
    Cooking.check()

    # Creating an instance
    ice_breaker = Cooking("gpt-4o")

    # Calling recipe generator, simple LLM call
    # response = ice_breaker.recipe_generator()
    # print(response)

    # Calling recipe generator agent
    response = ice_breaker.recipe_generator_agent()
    # print(response.list)
    for recipe in response.list:
        print(recipe.name)
        print(recipe.description)
        print("-------------------")
