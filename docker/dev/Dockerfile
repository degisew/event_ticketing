# Pull base image
FROM python:3.12.3-slim-bullseye


# Install build dependencies b/c the base image lacks
RUN apt-get update && apt-get install -y \
    curl\
    build-essential \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set global environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/usr/src/app



# Set the working directory
WORKDIR $APP_HOME

# Create a user to run the application
RUN addgroup --system app && adduser --system --group app

# Create the static and media files directories
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

# Install dependencies
COPY ./requirements/ ./requirements/
RUN pip install pip --upgrade
RUN pip install --upgrade -r ./requirements/dev.txt


RUN pip install psycopg2

# Copy the rest of the application code
COPY . .

# change the ownership all the files to the app user
RUN chown -R app:app $APP_HOME

EXPOSE 8000