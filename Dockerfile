# Start with Ubuntu image
FROM ubuntu:16.04

# Copy local directory into container directory called item-catalog
COPY . /item-catalog

# Set the directory that commands will be run from
WORKDIR /item-catalog

# Update
RUN apt-get update -y --fix-missing
RUN apt-get install -y python3 python3-pip build-essential
#RUN export PATH=~/environments/item-catalog/bin:$PATH
RUN pip3 install -U pip
# RUN pip3 uninstall -y setuptools
# RUN pip3 install 'setuptools<20.2'
RUN pip3 install -r requirements.txt

# Expose port for web server to serve application
EXPOSE 8000

# Run the application
CMD ["python3", "run.py"]