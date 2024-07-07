from langchain.prompts.prompt import Prompt, PromptTemplate
from langchain_openai import ChatOpenAI
from agents.recipe_lookup_agent import lookup as recipe_lookup_agent
from agents.recipe_preparation_agent import lookup as recipe_preparation_agent
from chains.custom_chains import CustomChains

from output_parsers import RecipesNameData, RecipesInstructionsData


class Cooking:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        print(f"Using model: {self.model}")

    @staticmethod
    def check():
        print("Hello, Langchain!")

    def recipe_generator(self, ingredients: str):
        """A simple LLM call"""
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

    def recipe_creator(self, ingredients: str, ethnicity: str):
        """Generating recipes using an agent with web tool"""
        # Gives a list of names of 3 recipes/dishes
        recipe_response = recipe_lookup_agent(ingredients, ethnicity, self.model)

        dishes_chain = CustomChains(self.model).get_dish_chain()
        parsed_response: RecipesNameData = dishes_chain.invoke(
            input={"recipe_list_data": recipe_response}
        )

        final_data = []
        # Finding instructions to prepare dishes
        for recipe in parsed_response.list:
            recipe_instructions_response = recipe_preparation_agent(
                recipe.name, self.model
            )

            dishe_instruction_chain = CustomChains(self.model).get_dish_instructions()
            parsed_instruction_response: RecipesInstructionsData = (
                dishe_instruction_chain.invoke(
                    input={"recipe_instructions": recipe_instructions_response}
                )
            )

            final_data.append(
                {
                    "name": recipe.name,
                    "description": recipe.description,
                    "ingredients": parsed_instruction_response.ingredients_list,
                    "instructions": parsed_instruction_response.instructions_list,
                }
            )
        return final_data


if __name__ == "__main__":
    # Calling static method
    Cooking.check()

    # Creating an instance
    ice_breaker = Cooking("gpt-4o")

    # Calling recipe generator, simple LLM call
    # ingredients = input("Enter ingredients: ")
    # response = ice_breaker.recipe_generator(ingredients)
    # print(response)

    # Calling recipe generator agent
    ingredients = input("Enter ingredients: ")
    ethnicity = input("Enter ethnicity/cuisine: ")
    response = ice_breaker.recipe_creator(ingredients, ethnicity)
    print(response)
