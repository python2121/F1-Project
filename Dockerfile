FROM python:3.12-slim
WORKDIR /app

RUN apt-get update
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# Copy in the source code
RUN git clone https://github.com/python2121/F1-Project.git .

RUN pip3 install -r src/requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]