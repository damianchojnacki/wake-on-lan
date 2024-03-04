FROM python:alpine3.19

# Update package list and install ether-wake and python3
RUN apk add --update --no-cache awake && \
  pip3 install uvicorn fastapi httpx --no-cache

# Create a directory for the Python script
WORKDIR /app

# Copy the Python script (app.py) to the container
COPY . .

# Expose port 8080 (can be changed) for the HTTP server
EXPOSE 8080

# Command to run when the container starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]