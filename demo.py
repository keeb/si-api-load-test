from si_api_demo.util import SI
import time
import matplotlib.pyplot as plt


api = SI()
change_set_id = api.create_change_set("load test")


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

for i in range(0, 10):
    start = time.time()
    print(f"creating asset #{i}")
    create_asset(asset_list[i])
    end = time.time()
    print(f"Execution time: {(end - start) * 1000:.2f} ms")
    exec_time_ms = (end - start) * 1000
    times.append(exec_time_ms)

plt.plot(times)
plt.xlabel("Run")
plt.ylabel("Execution Time (ms)")
plt.title("Function Execution Time Over Repeated Runs")
plt.savefig("execution_times.png")

# api.abandon_change_set()
