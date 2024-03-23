from fastapi import HTTPException
import plotly.graph_objects as go
from .utils import normalize_ratings, calculate_cluster_centroids
from .data_processing import extract_topics
from .workflow import process_courses  


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


def create_plot(n_clusters, df, cluster_labels):
   

        # Get the reduced vectors, descriptions, and links
        vectors = df['reduced_vectors'].tolist()
        descriptions = df['description'].tolist()
        links = df['link'].tolist()
        titles = df['title'].tolist()

        # Calculate cluster centroids
        centroids = calculate_cluster_centroids(cluster_labels, vectors)

        #normalized_ratings = normalize_ratings(df['rating'].tolist())

        # Create Plotly figure
        fig = go.Figure()

       # Add each point and a line from the origin to the point
        for v, title, link, label in zip(vectors, titles, links, cluster_labels):
            base_color = get_color_for_label(label, n_clusters)
            # Extract RGB components and update the alpha value based on rating
            r, g, b, _ = base_color.strip('rgba()').split(',')
            alpha = 0.7  # Adjust opacity based on rating
            color_with_alpha = f'rgba({r}, {g}, {b}, {alpha})'

            # The point itself
            fig.add_trace(go.Scatter(
                x=[v[0]], y=[v[1]],
                mode='markers',
                marker=dict(size=16, opacity=0.7, color=color_with_alpha),
                hovertext=[title],  # Use hovertext for descriptions
                hoverinfo='text',  # Show hovertext
                customdata=[link]
            ))

        # Add cluster summaries as text annotations
        # for label, centroid in centroids.items():
        #     cluster_descs = [desc for desc, l in zip(descriptions, cluster_labels) if l == label]
        #     summary = extract_topics(cluster_descs)
            
        #     fig.add_trace(go.Scatter(
        #         x=[centroid[0]], y=[centroid[1]],
        #         mode='text',
        #         text=[summary],
        #         textposition='middle center'
        #     ))
        
        
        # Update layout to remove legend
        fig.update_layout(showlegend=False)

        # Update layout to remove background grid lines
        fig.update_xaxes(showgrid=False)  # Remove x-axis grid lines
        fig.update_yaxes(showgrid=False)  # Remove y-axis grid lines

        # Update layout to remove x-axis and y-axis (including ticks and labels)
        fig.update_layout(
            xaxis=dict(
                visible=False,  # Hide the x-axis line, ticks, and labels
                showticklabels=False  # Hide x-axis tick labels
            ),
            yaxis=dict(
                visible=False,  # Hide the y-axis line, ticks, and labels
                showticklabels=False  # Hide y-axis tick labels
            )
        )

        # Update the layout to set the aspect ratio to square
        fig.update_layout(
            autosize=False,  # Disable autosize to set custom width and height
            width=600,       # Set figure width
            height=600,      # Set figure height (equal to width for square aspect ratio)
            xaxis=dict(
                scaleanchor="y",  # Ensure x-axis scale is anchored to y-axis scale
                scaleratio=1,  # Ensure x-axis and y-axis have the same scale ratio
            ),
            yaxis=dict(
                constrain='domain'  # Adjust the domain of the y-axis to fit with the scaling
            )
        )

        fig.update_layout(clickmode='event+select')

        return fig
    