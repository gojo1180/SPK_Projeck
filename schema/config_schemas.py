from pydantic import BaseModel

class WeightsSchema(BaseModel):
    C1: int
    C2: int
    C3: int
    C4: int
    C5: int

class TimingSchema(BaseModel):
    pre_workout: WeightsSchema
    post_workout: WeightsSchema

class DefaultWeightsSchema(BaseModel):
    cutting: TimingSchema
    bulking: TimingSchema
    maintenance: TimingSchema