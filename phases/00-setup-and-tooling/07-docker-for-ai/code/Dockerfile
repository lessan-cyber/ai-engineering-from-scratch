FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Prevent interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON=3.12

# Install minimal OS prerequisites
RUN apt update && apt install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binaries directly from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Automatically download, install, and configure Python 3.12 globally via uv
RUN uv python install 3.12 && uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /workspace

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --torch-backend=cu124 \
    torch==2.4.0 \
    torchvision==0.19\
    torchaudio==2.4.0


# Install data science and ML toolkit
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install \
    numpy \
    pandas \
    scikit-learn \
    matplotlib \
    jupyter \
    transformers \
    datasets \
    accelerate \
    safetensors

VOLUME ["/workspace", "/models"]

EXPOSE 8888

CMD ["python"]
