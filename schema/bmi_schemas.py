from pydantic import BaseModel, Field

class BMICalculateRequest(BaseModel):
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    unit: str = Field(default="metric", pattern="^(metric|imperial)$")


class BMIResponse(BaseModel):
    id_bmi: int
    nilai_bmi: float
    kategori: str
    saran: str
