# Chatbot with LangChain, OpenAI API, and Streamlit

## Overview

This project demonstrates the implementation of a chatbot using LangChain and the OpenAI API, with Streamlit for the
user interface.

## Getting Started

### Prerequisites

- Python 3.11.9
- OpenAI API key

### Project Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   ```bash
   .\.venv\Scripts\activate
   ```
   
3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
    ```

4. Copy `.env.template` and rename it to `.env`.
   ≥ Make sure to add your OpenAI API key to the file.

5. To start the assistant, run this command in your terminal:
   ```bash
   python main.py
   ```

6. To launch the assistant with a graphical interface, use this command:
   ```bash
    streamlit run chatbot_interface.py
    ```
