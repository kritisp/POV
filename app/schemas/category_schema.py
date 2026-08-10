from pydantic import BaseModel

class CategoryBase(BaseModel):
    id: str  # e.g., "shirt", "jeans"
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    class Config:
        from_attributes = True
