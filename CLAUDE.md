# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup and Environment

This is a Python-based load testing tool for the System Initiative API. Two environment setups are supported:

### Standard Setup
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create a `key` file with your workspace API key. Override the base URL if needed:
```bash
export SI_BASE_URL="https://api.systeminit.com"
```

### Direnv Setup (Alternative)
```bash
pip install -r requirements.txt
cat <<EOF >.env
export SI_API_KEY="$my_key"
EOF
```

## Running the Application

Primary entry point: `./dev.sh [OPTIONS] [-- PYTHON_ARGS]`

### Usage
```bash
./dev.sh [-s|--script SCRIPT] [-e|--environment ENV] [-k|--key KEY] [-- PYTHON_ARGS]
```

### Options
- `-s, --script` - Script to run (default: demo)
  - `demo` - Load testing script
  - `api` - Simple API demonstration  
  - `infra` - Complex infrastructure deployment
  - `cli` - Interactive CLI with animated logo

- `-e, --environment` - Environment (default: local)
  - `local` - Local development (uses `http://jack:5380`)
  - `staging` - Staging environment (uses `https://api.staging.systeminit.com`)
  - `prod` - Production environment (uses `https://api.systeminit.com`)

- `-k, --key` - Key name from keys/ directory
  - If not specified, uses `keys/default-local` or legacy `key` file

- `--` - Pass remaining arguments to Python script

### Key Management
Keys are stored in the `keys/` directory and can be named descriptively:
- `keys/keeb-homelab` - Homelab workspace key
- `keys/nh-prod-testing` - Production testing key
- `keys/default-local` - Default key for local development

Key resolution order:
1. Specified key name: `-k my-key` → `keys/my-key`
2. Default local key: `keys/default-local`
3. Legacy `key` file (backward compatibility)

### Examples
```bash
# Basic usage
./dev.sh                                    # Run demo script with local env and default key
./dev.sh -s api -e prod -k nh-prod-testing # Run API script with prod env and specific key
./dev.sh -s infra -k keeb-homelab          # Run infra script with local env and specific key

# Passing arguments to Python scripts
./dev.sh -s demo -- --components 100       # Pass --components 100 to demo.py
./dev.sh -k my-key -- --verbose --debug    # Pass multiple args to demo.py
./dev.sh -- --help                         # Pass --help to demo.py

# Help
./dev.sh -h                                 # Show help and available keys
```

## Code Architecture

### Core Components

**`src/si_api_demo/util.py`** - Main API client library
- `Session` class: Manages user session data from `/whoami` endpoint
- `SI` class: Main API client with methods for:
  - Creating change sets
  - Creating components with AWS resources
  - Executing management functions
  - Deleting/abandoning change sets

**`demo.py`** - Load testing script
- Configurable parameters: `NUM_COMPONENTS`, `NUM_WORKERS`, `ONE_COMPONENT`
- Creates AWS credentials and region components as dependencies
- Uses ThreadPoolExecutor for concurrent component creation
- Generates timing plots with matplotlib
- Reads asset names from `asset_list` file

**`api-demo.py`** - Simple API demonstration
- Creates a basic AWS VPC template component
- Demonstrates component creation and management function execution

**`src/si_api_demo/middleware.py`** - Middleware/helper functions for complex AWS infrastructure
- `make_change_set()`: Creates or finds existing change sets by name
- `make_cred_region()`: Creates AWS Credential and Region components
- `create_vpc()`: Creates AWS Standard VPC Template components
- `create_cluster()`: Creates AWS Standard ECS Cluster Template components
- `create_task_def()`: Creates AWS Standard ECS Task Definition Template components
- `create_ecs_service()`: Creates AWS Standard ECS Service Template components
- `run_and_log()`: Executes management functions on components with timing delays

### Key Patterns

1. **Authentication**: Uses Bearer token authentication with `SI_API_KEY`
2. **Component Creation**: All components require connections to AWS Credential and Region
3. **Change Sets**: All operations happen within a change set context
4. **Error Handling**: Basic exception handling with meaningful error messages

### Configuration

- Base URL configurable via `SI_BASE_URL` environment variable
- API key from `SI_API_KEY` environment variable or `key` file
- Debug mode available via `DEBUG` variable in util.py

## Development Notes

- The codebase uses `requests` library for HTTP calls
- Components are created with schema names and domain configurations
- Management functions can be executed on components (e.g., "Component Sync")
- Load testing generates timestamped execution time plots