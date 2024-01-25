def normalize_ratings(ratings):
    min_rating = min(ratings)
    max_rating = max(ratings)
    return [(r - min_rating) / (max_rating - min_rating) for r in ratings]

