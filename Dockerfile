FROM python:3.12.2

# Set the current working directory to /app/src.
# This is where we'll put src directory.
WORKDIR /app/src

# Copy the file with the requirements to the /app directory.
# Copy only the file with the requirements first, not the rest of the code.
# As this file doesn't change often, Docker will detect it and use the cache for this step, enabling the cache for the next step too.
COPY ./requirements.txt /app/requirements.txt

COPY ./model.pkl /app/model.pkl

# Install the package dependencies in the requirements file.
# The --no-cache-dir option tells pip to not save the downloaded packages locally as we working with containers.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the ./src directory inside the /app directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
# So, it's important to put this near the end of the Dockerfile, to optimize the container image build times.
COPY ./src /app/src

# run the uvicorn server.
# option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it that the application is running behind HTTPS, etc.
CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]