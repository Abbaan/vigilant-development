from pydantic import BaseModel, validator
import pandas as pd


class LearningResource(BaseModel):
    title: str
    description: str
    url: str   

    @validator('url')
    def check_url(cls, value):
        if not value.startswith('http'):
            raise ValueError('URL must start with http')
        return value 


class LearningResourceCollection(BaseModel):
    resources: list[LearningResource]
    
    def add_resource(self, resource: LearningResource):
        self.resources.append(resource)
    
    def to_dataframe(self):
        return pd.DataFrame([resource.dict() for resource in self.resources])
    
    def __iter__(self):
        return iter(self.resources)

    