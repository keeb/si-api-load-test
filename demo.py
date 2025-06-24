#!/usr/bin/env python

from collections import namedtuple
from si_api_demo.util import SI
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='SI API Load Test')
    parser.add_argument('--components', '-c', type=int, default=600, 
                       help='Number of components to create (default: 600)')
    parser.add_argument('--workers', '-w', type=int, default=1,
                       help='Number of worker threads (default: 1)')
    parser.add_argument('--one-component', type=str, metavar='SCHEMA_NAME',
                       help='Create the same component repeatedly using the specified schema name')
    parser.add_argument('--changeset-name', type=str,
                       help='Custom name for the change set (default: auto-generated with timestamp)')
    parser.add_argument('--url', '-u', type=str, default='http://localhost:5380',
                       help='API base URL (default: http://localhost:5380)')
    parser.add_argument('--settle-time', type=int, default=0,
                       help='Time to wait after each component creation (default: 0 seconds)')
    parser.add_argument('--connection-type', type=str, choices=['prop', 'socket'], default='prop', help='Type of connection to create between components (default: prop)')
    parser.add_argument('--connect-region-and-changeset', action=argparse.BooleanOptionalAction, default=True,
                       help='Create and connect the Region and Changeset components (default: True)')
    return parser.parse_args()

args = parse_args()
NUM_COMPONENTS = args.components
NUM_WORKERS = args.workers
ONE_COMPONENT_SCHEMA = args.one_component

api = SI(base_url=args.url)

reusing_changeset = False
if args.changeset_name:
    change_set_name = args.changeset_name
    # Check if changeset already exists
    existing_change_set_id = api.find_change_set_by_name(change_set_name)
    if existing_change_set_id:
        print(f"Found existing changeset '{change_set_name}', reusing it.")
        change_set_id = existing_change_set_id
        api.change_set_id = change_set_id
        reusing_changeset = True
    else:
        print(f"Creating new changeset '{change_set_name}'.")
        change_set_id = api.create_change_set(change_set_name)
else:
    change_set_name_date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    change_set_name = f"Load Test {change_set_name_date}: T: {NUM_WORKERS} C: {NUM_COMPONENTS}"
    change_set_id = api.create_change_set(change_set_name)

REGION_AND_CREDENTIAL_SUBSCRIPTIONS = {
    "/domain/extra/Region": {
        "component": "Demo us-east-1",
        "propPath": "/domain/region"
    },
    "/secrets/AWS Credential": {
        "component": "Demo Account",
        "propPath": "/secrets/AWS Credential"
    }
}
REGION_AND_CREDENTIAL_SOCKET_CONNECTIONS = [
    {
        "from": {
            "component": "Demo Account",
            "socketName": "AWS Credential",
        },
        "to": "AWS Credential",
    },
    {
        "from": {
            "component": "Demo us-east-1",
            "socketName": "Region",
        },
        "to": "Region",
    },
]

def create_asset(name):
    if "\n" in name:
        name = name.split("\n")[0]
    component_name = name.split("::")[-1]
    asset_struct = {
        "schemaName": name,
        "name": component_name
    }
    if args.connect_region_and_changeset:
        match args.connection_type:
            case "prop":
                asset_struct["subscriptions"] = REGION_AND_CREDENTIAL_SUBSCRIPTIONS
            case "socket":
                asset_struct["connections"] = REGION_AND_CREDENTIAL_SOCKET_CONNECTIONS
            case _:
                raise ValueError(f"Invalid connection type: {args.connection_type}")
    return api.create_component(asset_struct)

# start by aws credential and Region (only if creating new changeset)
if args.connect_region_and_changeset:
    if not reusing_changeset:
        credential = {"schemaName": "AWS Credential", "name": "Demo Account"}

        region = {
            "schemaName": "Region",
            "name": "Demo us-east-1",
            "domain": {"region": "us-east-1"},
        }

        api.create_component(credential)
        api.create_component(region)
        time.sleep(0)
    else:
        print("Skipping AWS credential and region creation (assuming they exist in the reused changeset).")

with open("asset_list") as f:
    asset_list = f.readlines()
    f.close()


# Clean up asset list and validate schema name if specified
asset_list = [asset.strip() for asset in asset_list]
if ONE_COMPONENT_SCHEMA:
    # Check if the schema exists in the asset list
    schema_found = False
    for asset in asset_list:
        if "\n" in asset:
            asset = asset.split("\n")[0]
        if asset == ONE_COMPONENT_SCHEMA:
            schema_found = True
            break
    
    if not schema_found:
        print(f"Error: Schema '{ONE_COMPONENT_SCHEMA}' not found in asset_list.")
        print("Please check the asset_list file for valid schema names.")
        exit(1)

times = []

def timed_create(i, asset):
    start = time.time()
    print(f"[#{datetime.now(timezone.utc)}] creating asset #{i}")
    try:
        create_asset(asset)
        end = time.time()
        print(f"[#{datetime.now(timezone.utc)}] created asset #{i}. Execution time: {(end - start) * 1000:.2f} ms")
        exec_time_ms = (end - start) * 1000
        time.sleep(args.settle_time)
        return exec_time_ms
    except Exception as e:
        print(f"[#{datetime.now(timezone.utc)}] Error creating asset #{i}: {e}")
        return e


with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    if not ONE_COMPONENT_SCHEMA:
        futures = [
            executor.submit(timed_create, i, asset_list[i])
            for i in range(NUM_COMPONENTS)
        ]
    else:
        futures = [
            executor.submit(timed_create, i, ONE_COMPONENT_SCHEMA)
            for i in range(NUM_COMPONENTS)
        ]

    for future in futures:
        result = future.result()
        if isinstance(result, Exception):
            print(f"First error encountered: {result}")
            exit(1)
        times.append(result)


now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

plt.plot(times)
plt.xlabel("Component")
plt.ylabel("Execution Time (ms)")
plt.title(f"Number of threads: {NUM_WORKERS}, Number of Components: {NUM_COMPONENTS}")
plt.savefig(f"execution_times-{now}.png")

# api.abandon_change_set()
