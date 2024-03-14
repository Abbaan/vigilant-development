import streamlit as st
import plotly
from vigilant_dev.visualization import create_plot
from vigilant_dev.workflow import process_courses
from vigilant_dev.utils import perform_clustering
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")



# Function to read and return the content of the Markdown file
def read_markdown_file(markdown_file_path):
    with open(markdown_file_path, 'r') as file:
        return file.read()
    
# Path to your Markdown files
markdown_file_path = 'learning_resources'

@st.cache_data
def process_logic(markdown_file_path, n_clusters):
    df = process_courses(markdown_file_path)
    cluster_labels = perform_clustering(df['reduced_vectors'].tolist(), n_clusters)
    return df, cluster_labels


def get_md_file_name(df, curve_number):
    return df.iloc[curve_number]['filename']

with st.sidebar:
    n_clusters = st.slider(min_value=2, max_value=8, value=3, label='Number of Clusters')


df, cluster_labels = process_logic(markdown_file_path, n_clusters)
fig = create_plot(n_clusters, df, cluster_labels)

                          
col1, col2 = st.columns([2,1])

with col1:
    selected_points = plotly_events(fig)

with col2:
    if selected_points:
        file_name = get_md_file_name(df, int(selected_points[0]['curveNumber']))
        markdown_content = read_markdown_file('learning_resources/' + file_name)
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.markdown('Select a learning resource to view its content.')
