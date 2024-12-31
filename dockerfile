# Use a lightweight mongodb-community-server base image
FROM mongodb/mongodb-community-server:latest

# Define maintainer information
LABEL maintainer="test@gmail.com"

# Copy the MongoDB initialization scripts into the image
COPY ./main.py /docker-entrypoint-initdb.d/

# Ensure the scripts have the right permissions (if needed)
#RUN chmod -R 755 /docker-entrypoint-initdb.d/

# Optionally, add a custom MongoDB configuration file
# COPY ./mongod.conf /etc/mongod.conf

# Expose the default MongoDB port
EXPOSE 27017

# Default command for the container
CMD ["mongod"]