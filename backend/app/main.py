from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from fastapi import HTTPException

from schemas import ReviewRequest
from db import reviews_collection
from llm import generate_ai_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "API running"}

@app.post("/submit-review")
def submit_review(data: ReviewRequest):
    print("Received request:", data)

    ai_response = generate_ai_response(data.review, data.rating)
    print("AI Response:", ai_response)

    result = reviews_collection.insert_one({
        "name": data.name,
        "email": data.email,
        "rating": data.rating,
        "review": data.review,
        "ai_response": ai_response
    })

    print("💾 Saved to DB with ID:", result.inserted_id)

    return {
        "success": True,
        "message": ai_response
    }
# ADMIN DASHBOARD API
@app.get("/admin/reviews")
def get_all_reviews():
    reviews = []
    for r in reviews_collection.find().sort("_id", -1):
        reviews.append({
            "name": r.get("name"),
            "email": r.get("email"),
            "rating": r.get("rating"),
            "review": r.get("review"),
            "ai_response": r.get("ai_response"),
            "created_at": str(r.get("_id"))
        })
    return reviews
@app.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    try:
        result = reviews_collection.delete_one(
            {"_id": ObjectId(review_id)}
        )

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")

        return {"success": True, "message": "Review deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/reviews")
def get_reviews():
    reviews = []
    for r in reviews_collection.find():
        r["_id"] = str(r["_id"])
        reviews.append(r)
    return reviews
