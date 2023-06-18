# with python3.9.12
FROM python:3.9.12

# Define environment variable
ENV BINGX_APIURL "https://api-swap-rest.bingbon.pro"
ENV BINGX_APIKEY "ChangeMe"
ENV BINGX_SECRETKEY "ChangeMe"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 18105 available to the world outside this container
EXPOSE 18105

# entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]