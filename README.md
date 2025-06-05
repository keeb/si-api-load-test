# si-api-load-test

## Setup

- Set up Python enviroment and install packages:

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

- Make a `key` file with your workspace api key
- Make sure the `BASE_URL` in util.py is pointed to the right instance or
  export `SI_BASE_URL` to override the base URL, for example:

```sh
export SI_BASE_URL="https:://api.systeminit.com"
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
echo "export SI_BASE_URL='https:://api.systeminit.com'" >>.envrc
```

## Run

- Run `dev.sh`

```sh
./dev.sh
```
