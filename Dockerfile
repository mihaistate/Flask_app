# Use Python runtime as parent image
FROM python:3.11.9-slim

# Setting working directory in container
WORKDIR /app

# Copy current directory contents into container
COPY . .

# Install any packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

#Run app.py when container launches
CMD ["flask", "run", "--host", "0.0.0.0"]
