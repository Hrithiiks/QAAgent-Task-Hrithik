import os
import json
from langchain_openai import ChatOpenAI
# --- CHANGE 1: Import the new local embeddings library ---
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- We no longer need dotenv at all ---

# --- Configuration ---
TRANSCRIPT_PATH = os.path.join("..", "data", "transcript.txt")
VECTORSTORE_PATH = os.path.join("..", "data", "faiss_index")
JSON_OUTPUT_PATH = os.path.join("..", "test_cases", "generated_tests.json")
MD_OUTPUT_PATH = os.path.join("..", "test_cases", "generated_tests.md")


def create_vector_store():
    """Creates a FAISS vector store using a local embedding model."""
    try:
        with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
            transcript = f.read()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(transcript)
        
        # --- CHANGE 2: Use the local HuggingFace model for embeddings ---
        print("Loading local embedding model... (This might download the model on the first run)")
        # Using a popular, efficient model for embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        print("Creating local vector store...")
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        print(f"Vector store saved successfully to {VECTORSTORE_PATH}")
        return vectorstore
    except Exception as e:
        print(f"\n--- An error occurred during local vector store creation: {e} ---")
        return None

def generate_test_cases(vectorstore):
    """Generates test cases using a LOCAL LLM served by LM Studio."""
    llm = ChatOpenAI(
        model_name="gemma-2-9b-it",
        openai_api_key="not-needed",
        openai_api_base="http://localhost:1234/v1"
    )
    
    retriever = vectorstore.as_retriever()
    
    prompt_template = """
    You are QAgenie, a helpful AI assistant. Your task is to create a JSON object containing frontend test cases based on the provided text.
    Your entire output MUST be a single, valid JSON object. Do not add any text or comments before or after the JSON.

    The JSON must have a single root key called "test_cases", which is an array of test case objects.
    Each test case object must have these exact keys: "id", "title", "description", "category", "priority", "steps".
    For the "steps" key, provide an array of actions for automation. Use standard CSS selectors for "selector".

    Context: {context}
    Question: {question}
    """
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )

    print("Generating test cases with QAgenie's brain (Local LLM)... This may take a moment.")
    query = "Generate a comprehensive set of frontend test cases for the user flow described in the video transcript."
    result = qa_chain.invoke({"query": query})
    
    json_result_string = result['result']
    
    print("\n--- Raw output from Local LLM ---")
    print(json_result_string)
    print("---------------------------------\n")

    # Saving the results...
    with open(JSON_OUTPUT_PATH, "w") as f:
        f.write(json_result_string)
    print(f"JSON test cases saved to {JSON_OUTPUT_PATH}")
    
    try:
        data = json.loads(json_result_string)
        with open(MD_OUTPUT_PATH, "w") as f:
            f.write("# QAgenie Test Plan for Recruter.ai\n\n")
            for tc in data.get('test_cases', []):
                f.write(f"## {tc.get('id', 'N/A')}: {tc.get('title', 'Untitled')}\n")
                f.write(f"**Priority:** {tc.get('priority', 'N/A')} | **Category:** {tc.get('category', 'N/A')}\n\n")
                f.write("```gherkin\n")
                f.write(tc.get('description', ''))
                f.write("\n```\n\n")
        print(f"Markdown report saved to {MD_OUTPUT_PATH}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"\n--- LLM output was not valid JSON or had a missing key ({e}). Saving raw output to Markdown file for review. ---")
        # Save the raw output for debugging
        with open(MD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(json_result_string)
        print(f"Raw output saved to {MD_OUTPUT_PATH}")


if __name__ == "__main__":
    if os.path.exists(VECTORSTORE_PATH):
        print("Loading existing vector store...")
        # --- CHANGE 3: Use the same local model when loading the store ---
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = create_vector_store()
    
    if vectorstore:
        # Ensure your LM Studio server is running before this step!
        generate_test_cases(vectorstore)
    else:
        print("Could not proceed without a vector store. Please check the errors above.")