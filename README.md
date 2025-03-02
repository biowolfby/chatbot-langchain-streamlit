# Chatbot with LangChain, Mistral API, and Streamlit

## Overview

This project demonstrates the implementation of a chatbot using LangChain and the Mistral API, with Streamlit for the
user interface.

## Getting Started

### Prerequisites

- Python 3.11.9
- Mistral API key

### Project Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   ```bash
   .venv\Scripts\activate
   ```
   
3. Install the required dependencies:
   ```bash
    pip install -r requirements_.txt
    ```

4. Copy `.env.template` and rename it to `.env`.
   ≥ Make sure to add your Mistral API key to the file.

5. To start the assistant, run this command in your terminal:
   ```bash
   python main.py
   ```

6. To launch the assistant with a graphical interface, use this command:
   ```bash
    streamlit run chatbot_interface.py
    ```

# Docker Container Deployment Guide

## 🚀 Step 1: Create a Dockerfile
Create a file named `Dockerfile` in your project directory:

```dockerfile
# Use the official Python image as a base
FROM python:3.9  

# Set the working directory inside the container
WORKDIR /app  

# Copy the application files to the container
COPY . .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Set the command to run the application
CMD ["streamlit", "run", "chatbot_interface.py", "--server.port=8501"]
```

## 🚀 Step 2: Build the Docker Image
Run the following command in the terminal:
```bash
docker build -t my-python-app .
```

## 🚀 Step 3: Run the Docker Container Locally
```bash
docker run -d -p 5000:5000 my-python-app
```
- `-d` → Runs the container in detached mode.
- `-p 5000:5000` → Maps port **5000** from the container to the host.
- `my-python-app` → The name of the image to run.

## 🚀 Step 4: Check Running Containers
To see running containers:
```bash
docker ps
```
To check logs:
```bash
docker logs <container_id>
```

## 🚀 Step 5: Stop & Remove Containers
Stop a running container:
```bash
docker stop <container_id>
```
Remove a container:
```bash
docker rm <container_id>
```

## 🚀 Step 6: Remove Docker Image (Optional)
If you need to remove the built image:
```bash
docker rmi my-python-app
```

---

## ✅ Summary
1. **Create a `Dockerfile`** with the necessary commands.
2. **Build the image** using `docker build -t my-python-app .`
3. **Run the container locally** using `docker run -d -p 5000:5000 my-python-app`
4. **Check logs and manage containers** (`docker ps`, `docker logs`, `docker stop`, `docker rm`)
5. **(Optional) Remove Docker image** if needed

