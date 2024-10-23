from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Any

# Custom type for handling ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Base configuration for MongoDB documents
class MongoBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# User Schemas
class UserBaseSchema(MongoBaseModel):
    name: str
    email: str
    photo: str
    role: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class CreateUserSchema(UserBaseSchema):
    password: str
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(MongoBaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(UserBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "60d5f8e8b82d97b2f1d7c107",
                "name": "John Doe",
                "email": "johndoe@example.com",
                "photo": "profile.jpg",
                "role": "user"
            }
        }


class UserResponse(MongoBaseModel):
    status: str
    user: UserResponseSchema


class FilteredUserResponse(UserBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


# Post Schemas
class PostBaseSchema(MongoBaseModel):
    title: str
    content: str
    category: str
    image: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class CreatePostSchema(PostBaseSchema):
    user: Optional[PyObjectId] = Field(default_factory=PyObjectId)


class PostResponse(PostBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user: FilteredUserResponse

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdatePostSchema(MongoBaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    user: Optional[str] = None


class ListPostResponse(MongoBaseModel):
    status: str
    results: int
    posts: List[PostResponse]












# from datetime import datetime
# from typing import List
# from pydantic import BaseModel, EmailStr, constr
# # from bson.objectid import ObjectId
# from bson import ObjectId 


# class UserBaseSchema(BaseModel):
#     name: str
#     email: str
#     photo: str
#     role: str | None = None
#     created_at: datetime | None = None
#     updated_at: datetime | None = None

#     class Config:
#         orm_mode = True


# class CreateUserSchema(UserBaseSchema):
#     password: str
#     passwordConfirm: str
#     verified: bool = False


# class LoginUserSchema(BaseModel):
#     email: EmailStr
#     password: str


# class UserResponseSchema(UserBaseSchema):
#     id: str
#     pass


# class UserResponse(BaseModel):
#     status: str
#     user: UserResponseSchema


# class FilteredUserResponse(UserBaseSchema):
#     id: str


# class PostBaseSchema(BaseModel):
#     title: str
#     content: str
#     category: str
#     image: str
#     created_at: datetime | None = None
#     updated_at: datetime | None = None

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}


# class CreatePostSchema(PostBaseSchema):
#     user: ObjectId | None = None
#     pass


# class PostResponse(PostBaseSchema):
#     id: str
#     user: FilteredUserResponse
#     created_at: datetime
#     updated_at: datetime


# class UpdatePostSchema(BaseModel):
#     title: str | None = None
#     content: str | None = None
#     category: str | None = None
#     image: str | None = None
#     user: str | None = None

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}


# class ListPostResponse(BaseModel):
#     status: str
#     results: int
#     posts: List[PostResponse]
