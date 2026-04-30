from pydantic import BaseModel, Field, ConfigDict
import pandas as pd

class QueryResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: str = Field(pattern="^(success|error|warning)$")
    message: str
    data: pd.DataFrame | None = None