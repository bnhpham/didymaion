FROM python:3.11-slim
WORKDIR /app

# Install the application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy files from source dir on the host into WORKDIR
COPY . .

# Backend and frontend ports
EXPOSE 8000
EXPOSE 8501
