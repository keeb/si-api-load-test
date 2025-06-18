# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Load Test
```bash
./dev.sh
```
This script sets up the environment and runs the main load test script with default settings.

### Manual Setup and Run
```bash
export SI_API_KEY=$(cat key)
export PYTHONPATH=src
python demo.py [options]
```

### Command Line Options
- `--components`, `-c`: Number of components to create (default: 600)
- `--workers`, `-w`: Number of worker threads (default: 1)  
- `--one-component SCHEMA_NAME`: Create the same component repeatedly using the specified schema name
- `--changeset-name`: Custom name for the change set. If a changeset with this name already exists, it will be reused (default: auto-generated with timestamp)
- `--url`, `-u`: API base URL (default: http://localhost:5380)

## Architecture

This is a load testing tool for the System Initiative (SI) API that creates AWS components in parallel to measure performance.

### Core Components

- **SI API Client** (`src/si_api_demo/util.py`): Main API wrapper class that handles authentication, change sets, and component creation
- **Load Test Script** (`demo.py`): Orchestrates the load test by creating components concurrently and measuring execution times

### Key Configuration

Configuration is now handled via command line arguments rather than hardcoded constants:
- Components count: Configurable via `--components` flag
- Worker threads: Configurable via `--workers` flag  
- Component creation mode: Configurable via `--one-component SCHEMA_NAME` flag
- API endpoint: Configurable via `--url` flag

### Test Flow

1. Creates a new change set with timestamped name
2. Creates baseline AWS credential and region components
3. Uses ThreadPoolExecutor to create components concurrently
4. Measures execution time for each component creation
5. Generates a matplotlib graph of execution times vs component number

### Authentication

The tool expects an API key in a `key` file in the project root, which gets loaded via the `dev.sh` script.