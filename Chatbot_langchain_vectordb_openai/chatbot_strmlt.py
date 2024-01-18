import os
from dotenv import load_dotenv
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import ImageCaptionLoader
from langchain.docstore.document import Document
from langchain.chains import RetrievalQAWithSourcesChain
import faiss
from langchain.vectorstores.faiss import FAISS
from langchain.document_loaders.url import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Chat UI title
st.header("Interact with ChatGPT - Upload Files and Ask Questions")

# File uploader in the sidebar on the left
with st.sidebar:
    # Input for OpenAI API Key
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize ChatOpenAI model
llm = ChatOpenAI(temperature=0, max_tokens=3500, model_name="gpt-3.5-turbo-16k", streaming=True)

# Sidebar section for uploading files and providing a YouTube URL
with st.sidebar:
    uploaded_files = st.file_uploader("Please upload your files", accept_multiple_files=True, type=None)
    # youtube_url = st.text_input("YouTube URL")
    with st.form(key="form"):
        website_url = st.text_input("Website URL")
        submit = st.form_submit_button(label="Load Data")

    st.info("If you upload more files, please refresh the browser to reset the session", icon="📁")

if uploaded_files or website_url:

    # Load the data and perform preprocessing only if it hasn't been loaded before
    if "processed_data" not in st.session_state:
        # Load the data from uploaded files
        documents = []

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Get the full file path of the uploaded file
                file_path = os.path.join(os.getcwd(), uploaded_file.name)

                # Save the uploaded file to disk
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                # Check if the file is an image
                if file_path.endswith((".png", ".jpg")):
                    # Use ImageCaptionLoader to load the image file
                    if os.path.exists(file_path):
                        image_loader = ImageCaptionLoader([file_path])
                        # Load image captions
                        image_documents = image_loader.load()
                        # Append the Langchain documents to the documents list
                        documents.extend(image_documents)
                elif file_path.endswith((".pdf", ".docx", ".txt")):
                    # Use UnstructuredFileLoader to load the PDF/DOCX/TXT file
                    loader = UnstructuredFileLoader(file_path)
                    loaded_documents = loader.load()

                    # Extend the main documents list with the loaded documents
                    documents.extend(loaded_documents)

        if website_url:
            loaders = UnstructuredURLLoader(urls=[website_url])
            data = loaders.load()
            print("data == >>", data)
            text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=150)
            docs = text_splitter.split_documents(data)
            documents.extend(docs)

        # Chunk the data, create embeddings, and save in vectorstore
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1500, chunk_overlap=150)
        document_chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()

        if embeddings is not None and any(embeddings):
            vectorstore = FAISS.from_documents(document_chunks, embeddings)
        else:
            # Handle the case when embeddings list is empty
            print("Error: Embeddings list is empty or does not contain elements")

        # Store the processed data in session state for reuse
        st.session_state.processed_data = {
            "document_chunks": document_chunks,
            "vectorstore": vectorstore,
        }

    else:
        # If the processed data is already available, retrieve it from session state
        document_chunks = st.session_state.processed_data["document_chunks"]
        vectorstore = st.session_state.processed_data["vectorstore"]

    # Initialize Langchain's QA Chain with the vectorstore
    qa = RetrievalQAWithSourcesChain.from_llm(llm=llm,  retriever=vectorstore.as_retriever(), verbose=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask your questions?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query the assistant using the latest chat history
        result = qa({"question": prompt, "chat_history": [(message["role"], message["content"]) for message in st.session_state.messages]})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response = result["answer"]
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)    
        print(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.write("Please upload your files and Web URL .")