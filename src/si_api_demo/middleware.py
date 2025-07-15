from si_api_demo.util import SI
from time import sleep
import os

# Use environment variable for base URL, defaulting to localhost
base_url = os.getenv("SI_BASE_URL", "http://localhost:5380")
api = SI(base_url=base_url)

basic_subscriptions = {
    "/domain/extra/Region": {
        "component": "Infra us-east-1",
        "propPath": "/domain/region",
    },
    "/secrets/AWS Credential": {
        "component": "Demo Infra Account",
        "propPath": "/secrets/AWS Credential",
    },
}

basic_connections = [
    {
        "from": {
            "component": "Demo Infra Account",
            "socketName": "AWS Credential",
        },
        "to": "AWS Credential",
    },
    {
        "from": {
            "component": "Infra us-east-1",
            "socketName": "Region",
        },
        "to": "Region",
    },
]


def make_change_set(name):
    existing_change_set_id = api.find_change_set_by_name(name)

    if existing_change_set_id:
        api.change_set_id = existing_change_set_id
        return existing_change_set_id

    change_set_id = api.create_change_set(name)
    return change_set_id


def make_cred_region():
    credential = {"schemaName": "AWS Credential", "name": "Demo Infra Account"}

    region = {
        "schemaName": "Region",
        "name": "Infra us-east-1",
        "domain": {"region": "us-east-1"},
    }

    print("creating cred and region")
    api.create_component(credential)
    api.create_component(region)


def create_vpc(name):
    vpc = {
        "schemaName": "AWS Standard VPC Template",
        "name": name,
        "connections": basic_connections,
        "domain": {"Template/Default/Values/Name": "Demo"},
    }
    vpc_data = api.create_component(vpc)
    return vpc_data


def run_and_log(data, func_name):
    id = data["component"]["id"]
    print(f"got id {id}")

    sleep(10)
    func_run_id = api.execute_management_function(id, func_name)
    # print(f"got func_run_id {func_run_id}")
    sleep(20)

    # sleep(5)
    logs = api.get_logs(func_run_id)
    print(logs)
    return logs
    #


def create_cluster(cluster_name):
    cluster = {
        "schemaName": "AWS Standard ECS Cluster Template",
        "name": cluster_name,
        "connections": basic_connections,
        "domain": {
            "Template/Default/Values/Cluster Name": cluster_name,
            "Template/Default/Values/CloudWatch Container Insights": "Enhanced",
        },
    }
    cluster_data = api.create_component(cluster)
    return cluster_data


def create_task_def(family, image, name):
    task_def_connections = [
        {
            "from": {
                "component": "demo-ecs-task-execution-role",
                "socketName": "ARN",
            },
            "to": "Execution Role ARN",
        },
        {
            "from": {
                "component": "demo-ecs",
                "socketName": "Arn",
            },
            "to": "ECS Cluster ARN",
        },
    ]

    actual_task_def_connections = basic_connections + task_def_connections

    task_def = {
        "schemaName": "AWS Standard ECS Task Definition Template",
        "name": "Task Def",
        "connections": actual_task_def_connections,
        "domain": {
            "Template/Default/Values/Family": family,
            "Template/Default/Values/CPU": "256",
            "Template/Default/Values/Memory": "512",
            "Template/Default/Values/Containers": [
                {
                    "Image": image,
                    "Name": name,
                    "Port Mappings": [
                        {
                            "AppProtocol": "http",
                            "ContainerPort": 80,
                            "HostPort": 80,
                        }
                    ],
                }
            ],
        },
    }

    task_def_data = api.create_component(task_def)
    return task_def_data


def create_ecs_service(family, task_name, name):
    service_connections = [
        {
            "from": {
                "component": "demo-vpc",
                "socketName": "Vpc Id",
            },
            "to": "Vpc Id",
        },
        {
            "from": {
                "component": f"{family}-ecs-task-definition",
                "socketName": "Task Definition Arn",
            },
            "to": "Task Definition",
        },
        {
            "from": {
                "component": f"{family}-ecs-container-definition-{task_name}",
                "socketName": "Container Definitions",
            },
            "to": "Load Balanced Container Definitions",
        },
        {
            "from": {
                "component": "demo-ecs",
                "socketName": "Cluster Name",
            },
            "to": "Cluster Name",
        },
        {
            "from": {
                "component": "demo-subnet-pub-1",
                "socketName": "Subnet Id",
            },
            "to": "Subnets",
        },
        {
            "from": {
                "component": "demo-subnet-pub-2",
                "socketName": "Subnet Id",
            },
            "to": "Subnets",
        },
        {
            "from": {
                "component": "demo-subnet-pub-3",
                "socketName": "Subnet Id",
            },
            "to": "Subnets",
        },
    ]

    actual_service_connections = basic_connections + service_connections

    ecs_service = {
        "schemaName": "AWS Standard ECS Service Template",
        "name": "My Cluster",
        "connections": actual_service_connections,
        "domain": {
            "Template/Default/Values/ServiceName": name,
            "Template/Default/Values/DesiredCount": 6,
        },
    }
    service_data = api.create_component(ecs_service)
    return service_data
