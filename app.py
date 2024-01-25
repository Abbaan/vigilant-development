from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go
import json
import pandas as pd
import plotly
from vigilant_dev.utils import get_color_for_label, normalize_ratings
from vigilant_dev.workflow import process_courses, perform_clustering  # Adjust the import according to your package structure

app = FastAPI()

# Replace 'your_data.csv' with the path to your actual data file
DATA_FILE = 'personal_dev_resources.csv'

n_clusters = 4

def create_plot():
    try:
        # Process your data and get the reduced vectors, descriptions, and links
        df, mapping = process_courses(DATA_FILE)
        # Assume the reduced vectors are stored in a column named 'reduced_vectors'
        vectors = df['reduced_vectors'].tolist()
        descriptions = df['description'].tolist()
        links = df['link'].tolist()
        titles = df['title'].tolist()

        # Perform clustering
        cluster_labels = perform_clustering(vectors, n_clusters)  # Adjust n_clusters as needed

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


@app.get("/", response_class=HTMLResponse)
async def get_plot():
    try:
        fig = create_plot()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return f"""
        <html>
            <head>
                <title>3D Course Visualization</title>
                <style>
                    html, body {{
                        margin: 0;
                        padding: 0;
                        height: 100%;
                    }}
                    #divPlotly {{
                        height: 100vh;  /* 100% of the viewport height */
                        width: 100vw;   /* 100% of the viewport width */
                    }}
                </style>
            </head>
            <body>
                <div id='divPlotly'></div>
                <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
                <script type='text/javascript'>
                    var graphs = {graphJSON};
                    Plotly.newPlot('divPlotly', graphs, {{
                        responsive: true
                    }});
                </script>
            </body>
        </html>
        """
    except HTTPException as e:
        return f"<html><body><h2>Error: {e.detail}</h2></body></html>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
