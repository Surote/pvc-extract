# Use the official Python image
FROM registry.redhat.io/rhel9/python-312:9.5-1744198409

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5123

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5123","--log-level", "debug", "app:app"]