# Using Python runtime as parent image
FROM python:3.11-slim

# Left out setting working directory
# Might need to configure

# Install any packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Making port 5000 available for world outside this container
EXPOSE 5000

# Define environemnt variable
ENV FLASK_APP=app.py

# Run app.py when container launches
CMD ["flask", "run", "--host", "0.0.0.0"]
