import streamlit as st
from vigilant_dev.pipeline import ClusteringPipeline
from vigilant_dev.model import KMeansClustering
from vigilant_dev.data_loader import HeadingBasedExtraction
from vigilant_dev.plotter import ClusterPlotMaker
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")
    
# Path to your Markdown files
markdown_file_path = 'learning_resources'


if 'pipeline' not in st.session_state or not st.session_state.pipeline_run:
    # Run the pipeline since it hasn't been run before
    extraction_strategy = HeadingBasedExtraction()
    clustering_strategy = KMeansClustering()
    pipeline = ClusteringPipeline(markdown_file_path, extraction_strategy, clustering_strategy)
    pipeline.run()
    
    # Save the results to the session state if you need to use them later
    st.session_state['pipeline'] = pipeline
    
    # Set the flag indicating that the pipeline has been run
    st.session_state.pipeline_run = True
else:
    # If the pipeline has already run, you can retrieve results from the session state
    pipeline = st.session_state['pipeline']



with st.sidebar:
    n_clusters = st.slider(min_value=2, max_value=8, value=3, label='Number of Clusters')

@st.cache_data
def create_plot(n_clusters):
    cluster_labels = pipeline.run_cluster_algorithm(n_clusters)
    plot = ClusterPlotMaker(pipeline.transformed_data, pipeline.cluster_strategy)
    return plot.make_plot()

fig = create_plot(n_clusters)

                          
col1, col2 = st.columns([2,1])

with col1:
    selected_points = plotly_events(fig)

with col2:
    if selected_points:

        data_element = int(selected_points[0]['curveNumber'])
                           
        # Example title, description, and link
        title = pipeline.transformed_data.iloc[data_element]['title']
        description = pipeline.transformed_data.iloc[data_element]['description']
        link = pipeline.transformed_data.iloc[data_element]['url']

        # Construct the Markdown string
        markdown_text = f"""
        # {title}

        {description}

        [Link]({link})
        
        """

        # Display the Markdown in Streamlit
        st.markdown(markdown_text,unsafe_allow_html=True)

    else:
        st.markdown('Select a learning resource to view its content.')
