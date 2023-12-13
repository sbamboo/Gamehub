#!/bin/bash

# RusticComponents BuildTool v1.0 (By: Simon Kalmi Claesson)
# This is the main build script made for unix systems

# Default project path
script_dir=$(dirname "$(readlink -f "$0")")
config_file="$script_dir/build.conf"

# Detect the platform
platform=""
case "$(uname -s)" in
    Linux*)
        platform="lnx"
        ;;
    Darwin*)
        platform="mac"
        ;;
    *)
        platform="win"
        ;;
esac

# Set default value for prefixes
error_prefix="\033[0;31m[Error]:\033[0m "
info_prefix="\033[0;34m[Info]:\033[0m  "
impo_prefix="\033[0;31m[Info]:\033[0m  "

# For Linux and MacOS, use cat, grep, and cut
if [ -f "$config_file" ]; then
    project=$(cat "$config_file" | grep "project=" | cut -d '=' -f 2 | sed 's/[^a-zA-Z0-9_\/\\-\.]//g')
else
    echo "Error: Configuration file $config_file not found."
    exit 1
fi

# Ensure the project variable is not empty
if [ -z "$project" ]; then
    echo "Error: Project path not found in $config_file."
    exit 1
fi

# Check if any arguments are provided
if [ $# -eq 0 ]; then
    usage
fi

# Check for --stripAnsi argument
if [[ "$*" == *--stripAnsi* ]]; then
    error_prefix="[Error]: "
    info_prefix="[Info]:  "
    impo_prefix="[Info]:  "
fi
# Check for --y argument
response=""
if [[ "$*" == *--y* ]]; then
    response="y"
fi
if [[ "$*" == *--n* ]]; then
    response="n"
fi

printf "\n  RusticComponents BuildTool v1.0 (By: Simon Kalmi Claesson)\n-------------------------------------------------------------\nBuilding for project: ${project}\n-------------------------------------------------------------\n\n"

# Function to exit with newline
nexit() {
    printf "\n"
    exit "$1"
}

# Function to display usage
usage() {
    printf "Usage: $0 [--setup | --win | --mac | --lnx | --all | --remBuilds] [--stripAnsi] [--y | --n]\n"
    nexit 1
}

# Function to set up the environment on Linux
setup_linux() {
    printf "${info_prefix}Setting up Rust and Cargo...\n"

    # Install Rust and Cargo
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    source $HOME/.cargo/env

    # Add Rust targets
    rustup target add x86_64-unknown-linux-gnu
    rustup target add x86_64-apple-darwin
    rustup target add x86_64-pc-windows-gnu

    # Install Mingw-w64 toolchain for Windows target on Ubuntu
    printf "${info_prefix}Installing Mingw-w64 toolchain...\n"
    sudo apt-get update
    sudo apt-get install -y mingw-w64

    # Install build essentials on Ubuntu
    printf "${info_prefix}Installing build essentials on Ubuntu..."
    sudo apt-get install -y build-essential

    printf "${info_prefix}Rust, Cargo, Mingw-w64, and build essentials setup complete."
}

# Function to set up the environment on MacOS
setup_mac() {
    printf "${info_prefix}Setting up Rust and Cargo on MacOS...\n"

    # Install Rust and Cargo
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    source $HOME/.cargo/env

    # Add Rust targets
    rustup target add x86_64-apple-darwin

    printf "${info_prefix}Rust, Cargo setup complete on MacOS.\n"
}

# Function to build a specific target
build_target() {
    local target=$1

    printf "${info_prefix}Building for $target...\n"
    cargo build --target $target
    mkdir -p $project/target/$target

    printf "\n"
}

# Function to remove builds
# Function to remove builds
remBuilds() {
    if [ "$response" == "" ]; then
        printf "${impo_prefix}Do you really want to remove all builds? [y/n]: "
        read -r response
    else
        printf "${impo_prefix}Do you really want to remove all builds? [y/n]: ${response}\n"
    fi

    case "$response" in
        [yY])
            printf "${info_prefix}Removing builds...\n"
            rm -rf $project/target
            printf "${info_prefix}Builds removed.\n"
            ;;
        [nN])
            printf "${info_prefix}Build removal aborted.\n"
            ;;
        *)
            printf "${error_prefix}Invalid response. Please enter 'y' or 'n'.\n"
            ;;
    esac
}

# Check for invalid combinations
if [ "$#" -gt 1 ] && [[ "$*" == *--setup* || "$*" == *--all* ]]; then
    printf "${error_prefix}Invalid combination of arguments. --setup, --all, and --remBuilds must be used alone.\n"
    nexit 1
fi

# Replace --all with individual platform arguments
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    if [ "${args[$i]}" == "--all" ]; then
        args[$i]="--win --lnx --mac"
    fi
done

# Iterate through all arguments
for arg in "$@"; do
    case "$arg" in
        --remBuilds)
            remBuilds
            nexit 0
            ;;
        --setup)
            # Check the operating system and call the appropriate setup function
            case "$platform" in
                lnx)
                    setup_linux
                    ;;
                mac)
                    setup_mac
                    ;;
                *)
                    printf "${error_prefix}Unsupported operating system.\n"
                    nexit 1
                    ;;
            esac
            nexit 0
            ;;
        --win)
            if [ "$platform" == "win" ] || [ "$platform" == "lnx" ]; then
                build_target "x86_64-pc-windows-gnu"
            else
                printf "${error_prefix}Cannot build for Windows on this platform.\n"
            fi
            ;;
        --mac)
            if [ "$platform" == "mac" ]; then
                build_target "x86_64-apple-darwin"
            else
                printf "${error_prefix}Cannot build for MacOS on this platform.\n"
            fi
            ;;
        --lnx)
            if [ "$platform" == "lnx" ]; then
                build_target "x86_64-unknown-linux-gnu"
            else
                printf "${error_prefix}Cannot build for Linux on this platform.\n"
            fi
            ;;
        --all)
            # Build for all targets
            build_target "x86_64-unknown-linux-gnu"
            build_target "x86_64-apple-darwin"
            build_target "x86_64-pc-windows-gnu"
            ;;
        *)
            usage
            ;;
    esac
done

printf "${info_prefix}Builds completed, see console output for results.\n"
