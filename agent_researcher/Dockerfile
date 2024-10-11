# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for building Python packages with C++ extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/*


# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app/src

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["PYTHONPATH=/root/agent_researcher/src", "uvicorn", "agent_researcher.main:app", "--host", "0.0.0.0", "--port", "8000"]