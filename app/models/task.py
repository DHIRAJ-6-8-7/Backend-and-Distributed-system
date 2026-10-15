from pydantic import BaseModel, Field

class CreatedTaskVerify(BaseModel):
    title: str = Field(min_length=12, max_length=100,
                    description="The title of the task",
                    example="Complete the FastAPI project")
    completed: bool = False

    age: int = Field(default=18, ge=18, le=100, description=f"The age of the task", example=25)

class ResponseTaskVerify(BaseModel):
    id: int
    title: str
    completed: bool
    age: int

class UpdateTaskVerify(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=12,
        max_length=100
    )
    completed: bool | None = Field(default=None)
    age: int | None = Field(
        default=None,
        ge=18,
        le=100
    )

class ErrorDetail(BaseModel):
    code: str
    message: str
    status: int

class ErrorResponse(BaseModel):
    error: ErrorDetail
