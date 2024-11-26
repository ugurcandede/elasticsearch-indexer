import argparse
import json
from enum import Enum
from time import sleep

import requests

# Mapping environments and schema types
ENVIRONMENTS = {
    "local": "dev",
    "staging": "preprod",
    "prod": "prod",
}


class IndexTypes(Enum):
    TICKETS = "tickets"
    COMMENTS = "comments"
    USERS = "users"
    ORGANIZATIONS = "organizations"


def get_update_url(env, tenant_id, schema_type):
    """
    Constructs the URL for the update request.
    """
    if env not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment: {env}")
    return f"http://localhost:8080/indexes/{tenant_id}/{schema_type}?restart=true"


def send_request(env, token, index_type, tenant_id):
    """
    Sends a POST request to create index and index all resources with given index_type to Elasticsearch.
    """
    print(f"Processing tenant: {tenant_id}")
    url = get_update_url(env, tenant_id, index_type)

    try:
        response = requests.post(url, headers={"Authorization": f"Bearer {token}", "tenantId": tenant_id})
        response.raise_for_status()
        print(f"Processing completed for tenant: {tenant_id}")
    except requests.RequestException as e:
        print(f"Error processing tenant {tenant_id}: {e}")


def main():
    """
    Main function to parse arguments and process tenants.
    """
    parser = argparse.ArgumentParser(description="Elasticsearch indexer")
    parser.add_argument("--env", required=True, choices=ENVIRONMENTS.keys(), help="Environment (local, staging, prod)")
    parser.add_argument("--token", required=True, help="Authorization token")

    # not required, default is IndexTypes.ORGANIZATIONS
    parser.add_argument("--type", choices=IndexTypes, help="Index type", default=IndexTypes.ORGANIZATIONS)

    args = parser.parse_args()

    try:
        with open("data.json", "r") as file:
            tenant_ids = json.load(file)
            for tenant_id in tenant_ids:
                send_request(args.env, args.token, args.type.value, tenant_id)
                sleep(5)
                print("Sleeping for 5 seconds...")
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading tenant data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("All tenants processed.")


if __name__ == "__main__":
    main()
