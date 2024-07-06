from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class RecipeNameData(BaseModel):
    name: str = Field(description="names of the recipe")
    description: str = Field(description="description of the recipe")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
        }


recipe_name_data_parser = PydanticOutputParser(pydantic_object=RecipeNameData)
