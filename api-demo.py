from si_api_demo.util import SI


api = SI()
change_set_id = api.create_change_set("Demo the API")


component = {
    "schemaName": "AWS Standard VPC Template",
    "name": "Demo",
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
    # "viewName": "Demo network",
    "domain": {"Template/Default/Values/Name": "Demo"},
}

credential = {"schemaName": "AWS Credential", "name": "Demo Account"}

region = {
    "schemaName": "Region",
    "name": "Demo us-east-1",
    "domain": {"region": "us-east-1"},
}

api.create_component(credential)
api.create_component(region)


component_data = api.create_component(component)
component_id = component_data["component"]["id"]

from time import sleep

sleep(10)

api.execute_management_function(component_id, "Component Sync")
