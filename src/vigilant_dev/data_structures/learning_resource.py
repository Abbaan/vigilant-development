from dataclasses import dataclass
from typing import Optional
import pandas as pd

@dataclass
class LearningResource:
    title: str
    description: str
    url: str    


@dataclass
class LearningResourceCollection:
    resources: list[LearningResource]
    
    def add_resource(self, resource: LearningResource):
        self.resources.append(resource)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([resource.__dict__ for resource in self.resources])

    