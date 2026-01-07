class ReviewModel:
    """Review document structure for MongoDB"""
    def __init__(self, name: str, email: str, rating: int, review: str, ai_response: str):
        self.name = name
        self.email = email
        self.rating = rating
        self.review = review
        self.ai_response = ai_response
