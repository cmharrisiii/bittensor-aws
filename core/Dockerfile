# Use an official Python runtime as a parent image
FROM public.ecr.aws/docker/library/python:3.10-slim as production

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD python manage.py runserver 0.0.0.0:80