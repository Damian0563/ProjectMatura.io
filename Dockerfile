# Use the official Python image as the base image
FROM python:3.12-alpine3.22
# Copy the requirements file into the container
COPY myapp/requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY . .    
# Expose the port the app runs on
EXPOSE 8000
# Command to run the application
CMD ["python", "myapp/manage.py", "runserver", "0.0.0.0:8000"]