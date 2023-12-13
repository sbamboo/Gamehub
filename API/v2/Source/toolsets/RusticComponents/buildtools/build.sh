#!/bin/bash

# Default project path
project="/path/to/your/rust/project"

# Function to display usage
usage() {
    echo "Usage: $0 [--setup]"
    exit 1
}

# Function to set up the environment
setup_environment() {
    echo "Setting up Rust and Cargo..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    source $HOME/.cargo/env
    rustup target add x86_64-pc-windows-gnu
    echo "Rust and Cargo setup complete."
}

# Check if any arguments are provided
if [ $# -eq 0 ]; then
    echo "Building project for Linux, macOS, and Windows..."
else
    case "$1" in
        --setup)
            setup_environment
            exit 0
            ;;
        *)
            usage
            ;;
    esac
fi

# Build the project for Linux
echo "Building for Linux..."
cargo build --target x86_64-unknown-linux-gnu
mkdir -p $project/target/linux

# Build the project for macOS
echo "Building for macOS..."
cargo build --target x86_64-apple-darwin
mkdir -p $project/target/macos

# Build the project for Windows
echo "Building for Windows..."
cargo build --target x86_64-pc-windows-gnu
mkdir -p $project/target/windows

echo "Builds completed successfully."
