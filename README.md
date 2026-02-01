# RAG Assignment - Space Exploration Assistant 🚀

## Overview
This is a **Local Applicative RAG** project for the Information Retrieval course.
It answers questions about space exploration (NASA, SpaceX, Mars) based on indexed Wikipedia articles.

🎬 **[Watch the Project Presentation Video](./space_rag_presentation.mp4)**

📂 **[Project Data & Outputs (Google Drive)](https://drive.google.com/drive/folders/1cz9nvYsX-Ligx5-y8jgunX6wuxAJ3Giu?usp=drive_link)**

## Prerequisites
1.  **Python 3.10+**
2.  **Ollama**: This project requires a local LLM runner.
    *   Download from [ollama.com](https://ollama.com).
    *   Run `ollama pull llama3` (or `mistral`) in your terminal to get the model.
    *   Make sure Ollama is running in the background.

## Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ingest Data**:
    Run the Jupyter Notebook to download data and create the local vector index:
    *   Open `data_ingestion.ipynb` in VS Code or Jupyter Lab.
    *   Run all cells.
    *   This will create a `./chroma_db` folder.

3.  **Run the App**:
    ```bash
    /opt/anaconda3/bin/python -m streamlit run app.py
    ```

## Project Structure
*   `app.py`: The Streamlit web application (UI + RAG Logic).
*   `data_ingestion.ipynb`: Notebook for loading Wikipedia data, chunking, and indexing.
*   `requirements.txt`: Python package dependencies.
*   `chroma_db/`: Directory where the vector database is stored (created after running ingestion).

## Team Members
<<<<<<< HEAD
*   Amina O - ID: 212958755
*   Ossama Z - ID: 212608368
*   Smia I - ID: 212608368

=======
*   Amina Omari - ID: 212958755
*   Ossama Ziadat - ID: 212608368
*   Smia Idres - ID: 214077521
>>>>>>> 4ef38e8c95a017715500593f817d0bd3133efac5
