# Use the official Python image unauthen
FROM registry.access.redhat.com/ubi9/python-312@sha256:0d8c7c7490a2399292e5dd02014e768d53523bab0abb86328388820adf6f5650

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5123

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5123","--log-level", "debug", "app:app"]
