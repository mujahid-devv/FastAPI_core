from typing import Annotated, List, Literal, TypedDict, Union

from pydantic import BaseModel, Field, EmailStr


class AddressData(TypedDict):
    city: str
    country: str


class UserCreate(BaseModel):
    # Annotated attaches validation metadata to a type.
    name: Annotated[str, Field(min_length=3, max_length=10)]
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=100)]
    role: Literal["admin", "user"]
    hobbies: Union[str, List[str]]
    address: AddressData


class UserResponse(BaseModel):
    id: int
    name: str
    role: Literal["admin", "user"]
    hobbies: Union[str, List[str]]
    address: AddressData
