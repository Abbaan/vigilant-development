from abc import ABC, abstractmethod
import pandas as pd
from typing import List
import plotly.graph_objects as go
from .model import ClusterStrategy



class PlotMaker(ABC):
    """Abstract base class for a plotter."""
    
    @abstractmethod
    def run_figure_logic(self):
        """Create the figure logic."""
        pass

    @abstractmethod
    def run_figure_layout(self):
        """Create the figure layout."""
        pass

    @abstractmethod
    def make_plot(self):
        """Build the plot."""
        pass


class ClusterPlotMaker(PlotMaker):
    """Concrete implementation of a cluster plotter."""
    
    def __init__(self, transformed_data: pd.DataFrame, cluster_strategy: ClusterStrategy):
        self.transformed_data = transformed_data
        self.cluster_strategy = cluster_strategy
        if cluster_strategy.state != 'clustered':
            raise ValueError("Cluster strategy must be in 'clustered' state.")

    def run_figure_logic(self):
        """Create the figure logic."""
        # Get the reduced vectors, descriptions, and links
        vectors = self.transformed_data['reduced_vectors'].tolist()
        descriptions = self.transformed_data['description'].tolist()
        links = self.transformed_data['url'].tolist()
        titles = self.transformed_data['title'].tolist()

        # Create Plotly figure
        self.fig = go.Figure()

       # Add each point and a line from the origin to the point
        for v, title, link, label in zip(vectors, titles, links, self.cluster_strategy.cluster_labels):
            base_color = self.cluster_strategy.convert_label_to_color(label)
            # Extract RGB components and update the alpha value based on rating
            r, g, b, _ = base_color.strip('rgba()').split(',')
            alpha = 0.7  # Adjust opacity based on rating
            color_with_alpha = f'rgba({r}, {g}, {b}, {alpha})'

            # The point itself
            self.fig.add_trace(go.Scatter(
                x=[v[0]], y=[v[1]],
                mode='markers',
                marker=dict(size=16, opacity=0.7, color=color_with_alpha),
                hovertext=[title],  # Use hovertext for descriptions
                hoverinfo='text',  # Show hovertext
                customdata=[link]
            ))

    def run_figure_layout(self):
        """Create the figure layout."""
        # Update layout to remove legend
        self.fig.update_layout(showlegend=False)

        # Update layout to remove background grid lines
        self.fig.update_xaxes(showgrid=False)  # Remove x-axis grid lines
        self.fig.update_yaxes(showgrid=False)  # Remove y-axis grid lines

        # Update layout to remove x-axis and y-axis (including ticks and labels)
        self.fig.update_layout(
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
        self.fig.update_layout(
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

        self.fig.update_layout(clickmode='event+select')

    def make_plot(self):
        """Build the figure."""
        self.run_figure_logic()
        self.run_figure_layout()
        return self.fig