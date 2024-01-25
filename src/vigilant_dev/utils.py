def get_color_for_label(label, num_clusters):
    # Define a list of colors in RGBA format (with full opacity by default)
    colors = [
        'rgba(255, 0, 0, 1)',   # Red
        'rgba(0, 255, 0, 1)',   # Green
        'rgba(0, 0, 255, 1)',   # Blue
        'rgba(128, 0, 128, 1)', # Purple
        'rgba(255, 165, 0, 1)', # Orange
        # ... add more colors as needed ...
    ]
    return colors[label % len(colors)]

def normalize_ratings(ratings):
    min_rating = min(ratings)
    max_rating = max(ratings)
    return [(r - min_rating) / (max_rating - min_rating) for r in ratings]

