# si-api-load-test

## Setup

- Set up Python environment and install packages:

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

- Make a `key` file with your workspace api key
- Make sure the `BASE_URL` in util.py is pointed to the right instance or
  export `SI_BASE_URL` to override the base URL, for example:

```sh
export SI_BASE_URL="https://api.systeminit.com"
```

### Alternative: With Direnv

- Assumes [direnv](https://direnv.net/) is installed
- Install Python packages:

```sh
pip install -r requirements.txt
```

- Set your workspace API token in `.env` (pasting in your key over `$my_key`):

```sh
cat <<EOF >.env
export SI_API_KEY="$my_key"
EOF
```

- If you need to override the base URL to Luminork (defaults to local
  development stack), then add an `SI_BASE_URL` environment variable to `.env`,
  for example:

```sh
echo "export SI_BASE_URL='https://api.systeminit.com'" >>.envrc
```

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
