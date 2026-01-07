from pydantic import BaseModel, EmailStr, Field

class ReviewRequest(BaseModel):
    name: str = Field(
        ...,
        description="Full name of the user submitting the review",
        example="Ananta Nayak"
    )

    email: EmailStr = Field(
        ...,
        description="Valid email address of the reviewer",
        example="anantanayak337@gmail.com"
    )

    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Star rating given by the user (1 to 5)",
        example=5
    )

    review: str = Field(
        ...,
        min_length=5,
        description="Detailed textual feedback provided by the user",
        example="This product is excellent and very easy to use."
    )
