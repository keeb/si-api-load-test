# si-api-load-test

## Setup

* Make a `key` file with your workspace api key

## Usage

### Basic Usage
```bash
./dev.sh
```

### Command Line Options
```bash
python demo.py [options]
```

Options:
- `--components`, `-c`: Number of components to create (default: 600)
- `--workers`, `-w`: Number of worker threads (default: 1)  
- `--one-component SCHEMA_NAME`: Create the same component repeatedly using the specified schema name
- `--changeset-name`: Custom name for the change set. If a changeset with this name already exists, it will be reused (default: auto-generated with timestamp)
- `--url`, `-u`: API base URL (default: http://localhost:5380)

### Examples
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
