FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV NODE_VERSION=20
ENV HOME=/root
ENV PATH=/root/.bun/bin:/root/.opencode/bin:$PATH

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    bash \
    ripgrep \
    jq \
    nodejs \
    npm \
    python3 \
    python3-pip \
    build-essential \
    ca-certificates \
    apt-transport-https \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash

# Install OpenCode
RUN curl -fsSL https://opencode.ai/install | bash

# Install additional Node.js tools
RUN npm install -g typescript

# Create directory structure
RUN mkdir -p /workspace/.opencode/{plugins,skills,agents,asp-servers,mcp-servers,scripts}

WORKDIR /workspace

# Copy configuration files
COPY opencode.json /workspace/
COPY opencode-plus.json /workspace/
COPY opencode-plus-plan.md /workspace/

# Copy enhanced GitHub action files
COPY .github/enhanced /workspace/.github/enhanced/

# Install plugin dependencies
RUN if [ -f /workspace/.opencode/package.json ]; then \
      cd /workspace/.opencode && bun install; \
    fi

# Install setup script
COPY scripts/install_plus.sh /workspace/scripts/
RUN chmod +x /workspace/scripts/install_plus.sh

# Create utility scripts
RUN echo '#!/bin/bash' > /workspace/opencode-validate && \
    echo '#!/bin/bash' > /workspace/opencode-run && \
    echo '#!/bin/bash' > /workspace/opencode-manage && \
    chmod +x /workspace/opencode-* && \
    opencode "$@" >> /workspace/opencode-run && \
    echo 'OpenCode Plus Environment' >> /workspace/opencode-validate

# Expose port for server
EXPOSE 4096

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD command -v opencode && opencode --version || exit 1

# Set default command
CMD ["/bin/bash"]