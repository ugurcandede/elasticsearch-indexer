## Elasticsearch Indexer

This Python script automates the creation of Elasticsearch indexes and the indexing of resources for specified tenants.
It processes tenant IDs from a JSON file and sends POST requests to a defined API endpoint.

### Features

- Supports different environments (local, staging, prod).
- Processes multiple tenants using data from a data.json file.
- Indexes different resource types (e.g., users, tickets, comments, organizations).
- Includes error handling for request failures and data file issues.

### Requirements

- Python 3.8 or higher
- Elasticsearch 7.6.2 or higher
- `requests` and `argparse` library for Python
- `data.json` file containing the tenant schemas. *(This file should be in the same directory as the script)*

### Generate `data.json` file:

This simple query can be used to generate the `data.json` file from the database. Then copy result and paste it to
`result.json` file

```sql
SELECT json_agg(schema_name)FROM main.tenant;
```

```json
[
  "tenant1",
  "tenant2",
  "tenant3"
]
```

### Usage:

- Install the `requests` and `argparse` libraries for Python.
    - or run the following command:
    - `pip install -r requirements.txt`
- Run the script with the following arguments:

```bash
python main.py --env <environment> --token <authorization_token> [--type <index_type>]
```

- **env**:  Environment to target (local, staging, prod).
- **token**: Authorization token for API requests.
- **type (Optional)**: Type of resource to index. Defaults to `organizations`. Available options:
    - users
    - tickets
    - comments
    - organizations

#### Example:

```bash
python main.py --env local --token abc123 --type users
```