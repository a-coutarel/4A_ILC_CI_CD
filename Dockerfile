FROM python:3.8

# Install dependencies
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask

# Copy the application code
COPY . .

# Set the environment variables
ENV FLASK_APP=api_transaction.py
ENV FLASK_ENV=development

# Expose the port on which the app will run
EXPOSE 5000

# Set the command to run when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

#docker build -t api_transaction .
#docker run -p 5000:5000 api_transaction