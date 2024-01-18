## Project :
This project seamlessly integrates OpenAI's GPT-3.5 language model with a Flask web server and Streamlit app, offering users an interactive chat interface. Notably, users can enhance the model's capabilities by uploading documents, which are processed and used for training. The system's architecture includes data preprocessing, vectorization, and a robust question-answering chain, providing a comprehensive and dynamic conversational experience.

## Overview :
Flask Web Server (app.py): Responsible for handling user requests and managing the integration of Streamlit and ChatGPT.

Streamlit App (chatbot_strmlt.py): Provides a user-friendly interface for uploading files, inputting questions, and receiving responses from ChatGPT. It runs in a separate thread alongside the Flask server.

Langchain and OpenAI Integration: The application uses Langchain to process and load data from various sources, including uploaded files and website URLs. It utilizes OpenAI's GPT-3.5 language model for generating responses to user queries.

## Getting Started :

These instructions will help you set up and run the project on your local machine.

### Prerequisites

prerequisites required to run the project, such as Python 3.10.0 or below than 3.11.0 for some libraries compatiblity, Flask and Streamlit, Langchain dependencies, OpenAI Python library or other software.

### Installation

A step-by-step guide to installing your project.

1. Create a virtual environment:
python -m venv venv

2. Activate the virtual environment:
On Windows:
venv\Scripts\activate

OnLinux:
source venv/bin/activate

3. Install project dependencies:
pip install -r requirements.txt

4. Create a .env file & Add : OPENAI_API_KEY="**********OPENAI_API_KEY**********"

5. Start the development server on your local run the command: "python app.py"
& 
redirect to http://localhost:8500/

### Usage
The main interface consists of a chat-like UI where users can ask questions.

# On the left sidebar File Upload and Processing:
Users can upload files (e.g., images, PDFs, text documents, Web URL) using the Streamlit app. The code processes these files, extracts relevant information, and stores it in Langchain's data structures.

Website URLs can be provided to fetch data and process it similarly to uploaded files.

Processed data is chunked, and embeddings are created using OpenAI's GPT-3.5 model. The resulting embeddings are saved in a Faiss vector store.

# On the right sidebar User Interaction:
Users interact with the system by asking questions through the Streamlit app. The application maintains a chat history and retrieves relevant information from the Faiss vector store.

The assistant responds to user queries based on the chat history and the stored embeddings.

## Note: 
Refresh the browser if you decide to upload more files to reset the session.

The system architecture involves Flask running the Streamlit app in a separate thread to allow concurrent execution.

Chat history and processed data are stored in the session state for better user experience and performance.


### Additional Information

1. Initialization
The OpenAI API key is set through the environment variable, and the ChatOpenAI model (llm) is initialized for interactive conversations using the OpenAI GPT-3.5-turbo-16k model.

2. Data Loading and Preprocessing
Users have the flexibility to upload files or input a website URL. Upon file uploads, content processing is tailored to the file type (image or text) using Langchain document loaders. If a website URL is provided, data is loaded and processed accordingly.

3. Vectorization and Embeddings
The data undergoes chunking into smaller pieces facilitated by a text splitter. OpenAI embeddings are then generated for these data chunks. These embeddings play a key role in creating an efficient vector store (FAISS) for streamlined retrieval.

4. Question-Answering (QA) Chain Initialization
A RetrievalQAWithSourcesChain is instantiated using the Langchain model (llm) and the vector store, laying the foundation for effective question-answering capabilities.

5. User Interaction
Users engage with the system by entering questions through an intuitive chat-like interface. The application adeptly maintains a chat history that encapsulates both user and assistant messages.

6. Query and Response
User queries serve as inputs for the QA Chain, leveraging the vector store for information retrieval. The assistant crafts responses based on the extracted information.

7. Display
The application thoughtfully presents user and assistant messages within the chat interface, ensuring a seamless and coherent interaction. The assistant's responses are prominently displayed for user understanding.

8. Session State Management
Streamlit's session state proves instrumental in storing processed data and chat history, contributing to efficient data reuse throughout the session.

9. Instructions and Information
Users are provided guidance to refresh the browser if opting to upload additional files, thereby resetting the session. The README file serves as a comprehensive guide, offering an application overview, setup instructions, and additional valuable information.