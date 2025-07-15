# si-api-load-test

A Python-based load testing tool for the System Initiative API with support for multiple environments and workspaces.

## Setup

### Standard Setup
Set up Python environment and install packages:

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Alternative: With Direnv
Assumes [direnv](https://direnv.net/) is installed:

```sh
pip install -r requirements.txt
cat <<EOF >.env
export SI_API_KEY="$my_key"
EOF
```

## Key Management

Create a `keys/` directory and store your workspace API keys with descriptive names:

```sh
mkdir keys
echo "your-api-key-here" > keys/default-local
echo "your-prod-key-here" > keys/workspace1-prod
echo "your-staging-key-here" > keys/workspace2-staging
```

## Usage

Run scripts using the `./dev.sh` command with options:

```sh
./dev.sh [-s|--script SCRIPT] [-e|--environment ENV] [-k|--key KEY] [-- PYTHON_ARGS]
```

### Options

- `-s, --script` - Script to run (default: demo)
  - `demo` - Load testing script
  - `api` - Simple API demonstration  
  - `infra` - Complex infrastructure deployment
  - `cli` - Interactive CLI with animated logo

- `-e, --environment` - Environment (default: local)
  - `local` - Local development (`http://jack:5380`)
  - `staging` - Staging environment (`https://api.staging.systeminit.com`)
  - `prod` - Production environment (`https://api.systeminit.com`)

- `-k, --key` - Key name from keys/ directory
- `--` - Pass remaining arguments to Python script

### Examples

```sh
# Basic usage
./dev.sh                                    # Run demo with local env and default key
./dev.sh -s api -e prod -k workspace1-prod # Run API demo with prod env and specific key
./dev.sh -s infra -k my-workspace          # Run infra demo with local env and specific key

# Passing arguments to Python scripts
./dev.sh -s demo -- --components 100       # Pass --components 100 to demo.py
./dev.sh -- --help                         # Pass --help to demo.py

# Help
./dev.sh -h                                 # Show help and available keys
```

### Direct Python Usage

You can also run demo.py directly with these options:
- `--components`, `-c`: Number of components to create (default: 600)
- `--workers`, `-w`: Number of worker threads (default: 1)  
- `--one-component SCHEMA_NAME`: Create the same component repeatedly using the specified schema name
- `--changeset-name`: Custom name for the change set. If a changeset with this name already exists, it will be reused (default: auto-generated with timestamp)
- `--url`, `-u`: API base URL (default: http://localhost:5380)

```bash
# Run with 100 components using 4 worker threads
python demo.py --components 100 --workers 4

# Test against production API
python demo.py --url https://api.systeminit.com

# Create the same component 50 times with 2 workers
python demo.py --components 50 --workers 2 --one-component "AWS::EC2::Instance"

# Use a custom changeset name
python demo.py --changeset-name "My Custom Load Test"
```

## Scripts

- **demo.py** - Load testing script with configurable components and workers
- **api-demo.py** - Simple API demonstration creating AWS VPC components
- **infra-demo.py** - Complex infrastructure deployment using middleware functions
- **cli.py** - Interactive CLI with animated logo and command processing
