# Setting the python runtime
FROM python:3.12-slim

# Setting the working directory in the container
WORKDIR /GraphTheoryProject/Wiki-Relations

# Copying the list of packages I will be using 
COPY ./requirements.txt ./

# Installing the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Copying the directory contents into the container
COPY src ./src

# Defining the command to run with the python script
CMD ["python", "src/main.py"]