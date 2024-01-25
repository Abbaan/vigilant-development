from fastapi import HTTPException
import plotly.graph_objects as go
from .utils import normalize_ratings, calculate_cluster_centroids
from .data_processing import extract_topics
from .workflow import process_courses, perform_clustering  


def get_color_for_label(label, num_clusters):
    # Define a list of colors in RGBA format (with full opacity by default)
    #Opacity will be used as visual cue for the rating
    colors = [
        'rgba(255, 0, 0, 1)',   # Red
        'rgba(0, 255, 0, 1)',   # Green
        'rgba(0, 0, 255, 1)',   # Blue
        'rgba(128, 0, 128, 1)', # Purple
        'rgba(255, 165, 0, 1)', # Orange
        # ... add more colors as needed ...
    ]
    return colors[label % len(colors)]


def create_plot():
    try:
        DATA_FILE = 'personal_dev_resources.csv'

        # predetermined number of clusters for now, perhaps this should
        # be configured via hierarchical clustering as a next step instead
        n_clusters = 4

        # Process data and get the reduced vectors, descriptions, and links
        df, mapping = process_courses(DATA_FILE)
        vectors = df['reduced_vectors'].tolist()
        descriptions = df['description'].tolist()
        links = df['link'].tolist()
        titles = df['title'].tolist()

        # Perform clustering
        cluster_labels = perform_clustering(vectors, n_clusters)  

        # Calculate cluster centroids
        centroids = calculate_cluster_centroids(cluster_labels, vectors)

        normalized_ratings = normalize_ratings(df['rating'].tolist())

        # Create Plotly figure
        fig = go.Figure()

       # Add each point and a line from the origin to the point
        for v, title, link, label, rating in zip(vectors, titles, links, cluster_labels, normalized_ratings):
            base_color = get_color_for_label(label, n_clusters)
            # Extract RGB components and update the alpha value based on rating
            r, g, b, _ = base_color.strip('rgba()').split(',')
            alpha = 0.4 + 0.6 * rating  # Adjust opacity based on rating
            color_with_alpha = f'rgba({r}, {g}, {b}, {alpha})'

            # Line from origin to the point
            fig.add_trace(go.Scatter3d(
                x=[0, v[0]], y=[0, v[1]], z=[0, v[2]],
                mode='lines',
                line=dict(color=color_with_alpha, width=2),
                hoverinfo='skip',  # Skip hover for lines
                showlegend=False
            ))

            # The point itself
            fig.add_trace(go.Scatter3d(
                x=[v[0]], y=[v[1]], z=[v[2]],
                mode='markers',
                marker=dict(size=5, opacity=0.8, color=color_with_alpha),
                hovertext=[title],  # Use hovertext for descriptions
                hoverinfo='text',  # Show hovertext
                customdata=[link]
            ))

        # Add cluster summaries as text annotations
        for label, centroid in centroids.items():
            cluster_descs = [desc for desc, l in zip(descriptions, cluster_labels) if l == label]
            summary = extract_topics(cluster_descs)
            
            fig.add_trace(go.Scatter3d(
                x=[centroid[0]], y=[centroid[1]], z=[centroid[2]],
                mode='text',
                text=[summary],
                textposition='middle center'
            ))

        # Update layout to remove spike lines
        fig.update_layout(
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, zeroline=False, showspikes=False),
                yaxis=dict(showbackground=False, showticklabels=False, zeroline=False, showspikes=False),
                zaxis=dict(showbackground=False, showticklabels=False, zeroline=False, showspikes=False),
            ),
            scene_aspectmode='data',
            margin=dict(l=0, r=0, b=0, t=0)
        )


        return fig
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))