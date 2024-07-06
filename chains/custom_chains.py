from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

from output_parsers import recipes_name_data_parser


class CustomChains:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(temperature=0, model_name=model_name)
        self.llm_creative = ChatOpenAI(temperature=1, model_name=model_name)

    def get_dish_chain(self) -> RunnableSequence:
        summary_template = """
                 given the list of the dishes with name and description, {recipe_list_data}
                 I want you to create a list of dishes with the following format
                 1. a name for the dish
                 2. a 1 line description for the dish
                 \n{format_instructions}
             """

        summary_prompt_template = PromptTemplate(
            input_variables=["recipe_list_data"],
            template=summary_template,
            partial_variables={
                "format_instructions": recipes_name_data_parser.get_format_instructions()
            },
        )

        return summary_prompt_template | self.llm | recipes_name_data_parser
