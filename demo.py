from si_api_demo.util import SI
import time
import matplotlib.pyplot as plt
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

NUM_COMPONENTS = 10
NUM_WORKERS = 3
ONE_COMPONENT = False

api = SI()

change_set_name_date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

change_set_id = api.create_change_set(
    f"Load Test {change_set_name_date}: T: {NUM_WORKERS} C: {NUM_COMPONENTS}"
)


def create_asset(name):
    if "\n" in name:
        name = name.split("\n")[0]
    component_name = name.split("::")[-1]
    asset_struct = {
        "schemaName": name,
        "name": component_name,
        "connections": [
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
        ],
    }
    api.create_component(asset_struct)


# start by aws credential and Region


credential = {"schemaName": "AWS Credential", "name": "Demo Account"}

region = {
    "schemaName": "Region",
    "name": "Demo us-east-1",
    "domain": {"region": "us-east-1"},
}

api.create_component(credential)
api.create_component(region)

with open("asset_list") as f:
    asset_list = f.readlines()
    f.close()

times = []


def timed_create(i, asset):
    start = time.time()
    print(f"creating asset #{i}")
    create_asset(asset)
    end = time.time()
    print(f"Execution time: {(end - start) * 1000:.2f} ms")
    exec_time_ms = (end - start) * 1000
    return exec_time_ms


with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    if not ONE_COMPONENT:
        futures = [
            executor.submit(timed_create, i, asset_list[i])
            for i in range(NUM_COMPONENTS)
        ]
    else:
        futures = [
            executor.submit(timed_create, i, asset_list[40])
            for i in range(NUM_COMPONENTS)
        ]

    for future in futures:
        times.append(future.result())


now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

plt.plot(times)
plt.xlabel("Component")
plt.ylabel("Execution Time (ms)")
plt.title(f"Number of threads: {NUM_WORKERS}, Number of Components: {NUM_COMPONENTS}")
plt.savefig(f"execution_times-{now}.png")

# api.abandon_change_set()
