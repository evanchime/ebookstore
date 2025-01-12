# Use the latest CPython image as the base
FROM python:latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# The main executable
ENTRYPOINT ["python3", "ebookstore.py"]
