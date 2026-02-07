#install python --> BASE layer

FROM python:3.10-slim

#Set working directory
WORKDIR /app/

#Copy your project from local directory to docker image. Copy from destination to APP folder that is why (.) period is used.
COPY ./src/ .

#install packes required to run the project.
RUN pip install --no-cache-dir -r requirements.txt

#Expose the port for run
EXPOSE 8000

#command which will start my application
CMD [ "python","./src/main.py" ]