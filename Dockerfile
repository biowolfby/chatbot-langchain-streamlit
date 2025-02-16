# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable for the container to use
ENV NAME World

# Run chatbot_interface.py when the container launches
CMD ["streamlit", "run", "chatbot_interface.py", "--server.port=8501"]
