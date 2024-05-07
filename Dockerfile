FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that your Flask app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
