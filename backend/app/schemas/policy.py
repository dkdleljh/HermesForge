from typing import List

from pydantic import BaseModel


class PolicyRule(BaseModel):
    code: str
    description: str


class PolicyResponse(BaseModel):
    policy_name: str
    version: str
    rules: List[PolicyRule]
