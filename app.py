import streamlit as st
import io
import os
from markitdown import MarkItDown

# Set a simple page configuration
st.set_page_config(
    page_title="Docs to Markdown Converter",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- UI Layout ---
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .stFileUploader {
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #f9f9f9;
    }
    .stDownloadButton button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stDownloadButton button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Docs to Markdown Converter")
st.markdown("Easily convert various documents to a clean Markdown text format. Just drag and drop your file below.")

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Drag and drop your file here",
    type=[
        "pptx", "docx", "xlsx", "pdf", "jpg", "jpeg", "png", "txt", "html", "csv", "json"
    ]
)

# Function to convert the file using MarkItDown
def convert_to_markdown(file_content):
    """
    Converts file-like object content to Markdown text using MarkItDown.
    """
    try:
        md = MarkItDown()
        result = md.convert(file_content)
        return result.text_content
    except Exception as e:
        return f"Error: Failed to convert the file. Please ensure the file type is supported. Details: {e}"

# Main processing logic
if uploaded_file is not None:
    # Use a spinner to indicate processing
    with st.spinner("Converting..."):
        # The file content needs to be read into a bytes-like object for MarkItDown
        bytes_data = io.BytesIO(uploaded_file.getvalue())

        # Convert the file content
        markdown_text = convert_to_markdown(bytes_data)

    st.success("Conversion complete!")
    
    # Check if the conversion was successful before offering download
    if not markdown_text.startswith("Error"):
        # --- Download Button ---
        # Get the original filename without the extension
        original_filename = os.path.splitext(uploaded_file.name)[0]
        download_filename = f"{original_filename}.md"
        
        # Create a BytesIO object with the full text content for the download button
        download_data = io.BytesIO(markdown_text.encode('utf-8'))
        
        st.download_button(
            label="Download Full Text",
            data=download_data,
            file_name=download_filename,
            mime="text/markdown",
            use_container_width=True
        )

        # --- Rendered Preview in an expandable section ---
        with st.expander("Rendered Preview"):
            st.markdown(markdown_text)
