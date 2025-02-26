# Stage 1: Build the Python Wheel
FROM python:3.12.8-slim-bullseye AS builder

LABEL authors="uwieske"

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install necessary dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /data

# Copy the project files into the container
COPY . .

# Install the `build` package and build the wheel
RUN pip install --no-cache-dir build --quiet \
    && python -m build

# Stage 2: Runtime Environment
FROM python:3.12.8-slim-bullseye

LABEL authors="uwieske"

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install runtime dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /ddd_llm_data

# Copy the built wheel from the builder stage
COPY --from=builder /data/dist/*.whl /tmp/

# Install the wheel
RUN pip install --no-cache-dir /tmp/*.whl \
    && rm -rf /tmp/*.whl

# Define the entry point (modify as needed for your app)
#CMD ["/bin/bash"]

EXPOSE 5000
EXPOSE 8000