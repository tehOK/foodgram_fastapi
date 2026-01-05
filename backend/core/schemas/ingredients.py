from pydantic import BaseModel, ConfigDict

class IngredientBase(BaseModel):
    id: int
    name: str
    measurement_unit: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class IngredientRead(IngredientBase):
    pass

class IngredientInRecipe(IngredientBase):
    amount: int

class IngredientForRecipe(BaseModel):
    id: int
    amount: int