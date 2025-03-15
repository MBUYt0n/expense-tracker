FROM python:3.10-slim
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir requests flask flask_cors nbconvert nbformat pandas numpy matplotlib
RUN git clone https://github.com/MBUYt0n/expense-tracker.git
WORKDIR /expense-tracker
EXPOSE 3000 
CMD ["python", "flasky.py"]
