FROM python:3.10-slim
RUN apt-get update && apt-get install -y git
RUN git config --global user.email "pes1202201377@pesu.pes.edu"
RUN git config --global user.name "MBUYt0n2"
RUN pip install --no-cache-dir requests flask flask_cors nbconvert nbformat pandas numpy matplotlib jupyter ipykernel
RUN git clone https://github.com/MBUYt0n/expense-tracker.git
WORKDIR /expense-tracker
EXPOSE 3000 
CMD ["python", "flasky.py"]
