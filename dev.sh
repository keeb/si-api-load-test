#!/usr/bin/env sh

# Default values
SCRIPT_NAME="demo"
ENV="local"
KEY_NAME=""

# Parse command line arguments
PYTHON_ARGS=""
while [ $# -gt 0 ]; do
    case $1 in
        -s|--script)
            SCRIPT_NAME="$2"
            shift 2
            ;;
        -e|--environment)
            ENV="$2"
            shift 2
            ;;
        -k|--key)
            KEY_NAME="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [-s|--script SCRIPT] [-e|--environment ENV] [-k|--key KEY] [-- PYTHON_ARGS]"
            echo ""
            echo "Options:"
            echo "  -s, --script      Script to run (default: demo)"
            echo "                    Options: demo, api, infra, cli"
            echo "  -e, --environment Environment (default: local)"
            echo "                    Options: local, staging, prod"
            echo "  -k, --key         Key name from keys/ directory"
            echo "                    If not specified, uses default-local or legacy key file"
            echo "  --                Pass remaining arguments to Python script"
            echo ""
            echo "Examples:"
            echo "  $0                                    # Run demo script with local env and default key"
            echo "  $0 -s api -e prod -k my-key         # Run API script with prod env and my-key"
            echo "  $0 -s infra -k keeb-homelab         # Run infra script with local env and keeb-homelab key"
            echo "  $0 -s demo -- --components 100      # Run demo script passing --components 100 to Python"
            echo ""
            echo "Available keys:"
            ls keys/ 2>/dev/null || echo "  No keys directory found"
            exit 0
            ;;
        --)
            shift
            PYTHON_ARGS="$*"
            break
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Set script file based on script name
case "$SCRIPT_NAME" in
    demo|d)
        SCRIPT="demo.py"
        ;;
    api|a)
        SCRIPT="api-demo.py"
        ;;
    infra|i)
        SCRIPT="infra-demo.py"
        ;;
    cli|c)
        SCRIPT="cli.py"
        ;;
    *)
        echo "Unknown script: $SCRIPT_NAME"
        echo "Available scripts: demo, api, infra, cli"
        exit 1
        ;;
esac

# Key selection (fallback to legacy 'key' file, then default-local)
if [ -n "$KEY_NAME" ]; then
    KEY_FILE="keys/$KEY_NAME"
elif [ -f "keys/default-local" ]; then
    KEY_FILE="keys/default-local"
elif [ -f "key" ]; then
    KEY_FILE="key"
else
    echo "No key specified and no default key found"
    echo "Available keys:"
    ls keys/ 2>/dev/null || echo "  No keys directory found"
    exit 1
fi

# Set environment-specific base URLs
case "$ENV" in
    local|l)
        export SI_BASE_URL="http://jack:5380"
        ;;
    staging|s)
        export SI_BASE_URL="https://api.staging.systeminit.com"
        ;;
    prod|production|p)
        export SI_BASE_URL="https://api.systeminit.com"
        ;;
    *)
        echo "Unknown environment: $ENV"
        echo "Available environments: local, staging, prod"
        exit 1
        ;;
esac

# Load the API key
if [ -f "$KEY_FILE" ]; then
    export SI_API_KEY="$(cat "$KEY_FILE")"
else
    echo "Key file not found: $KEY_FILE"
    exit 1
fi

export PYTHONPATH=src

echo "Running $SCRIPT with environment: $ENV, key: $(basename "$KEY_FILE")"
if [ -n "$PYTHON_ARGS" ]; then
    echo "Python arguments: $PYTHON_ARGS"
    python "$SCRIPT" $PYTHON_ARGS
else
    python "$SCRIPT"
fi
