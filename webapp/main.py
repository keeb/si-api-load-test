import requests
from flask import Flask, render_template, jsonify
import json
from si_api_demo.util import SI


api = SI()

app = Flask(__name__)


@app.route("/test")
def whoami():
    print(api.session)
    return jsonify(api.session)


@app.route("/")
def lightsail():
    return render_template("lightsail.html")


@app.route("/deployed")
def deployed():
    return render_template("deployed.html")


@app.route("/deploy")
def deploy():
    change_set_id = api.create_change_set("Provision Customer")

    """
    subscriptions = {
        "/domain/extra/Region": {
            "component": "IDP - us-east-1",
            "propPath": "/domain/region",
        },
        "/secrets/AWS Credential": {
            "component": "IDP Credential",
            "propPath": "/secrets/AWS Credential",
        },
    }

    component = {
        "schemaName": "AWS::EC2::Instance",
        "name": "Rokket EC2 Instance",
        "subscriptions": subscriptions,
        "viewName": "Rokket",
        "domain": {
            "ImageId": "ami-05ffe3c48a9991133",
            "InstanceType": "t3.micro",
            "UserData": "IyEvYmluL2Jhc2gKc2V0IC1ldXgKCiMgSW5zdGFsbCBjdXJsCmRuZiBpbnN0YWxsIC15IGN1cmwKCiMgSW5zdGFsbCBPbGxhbWEKY3VybCAtZnNTTCBodHRwczovL29sbGFtYS5jb20vaW5zdGFsbC5zaCB8IHNoCgojIEVuYWJsZSBPbGxhbWEgc3lzdGVtZCBzZXJ2aWNlIHRvIHN0YXJ0IG9uIGJvb3QKc3lzdGVtY3RsIGVuYWJsZSAtLW5vdyBvbGxhbWE=",
        },
    }
    api.create_component(component)
    """
    component = {
        "schemaName": "AWS::EC2::Instance",
        "name": "Rokket EC2 Instance",
        "connections": [
            {
                "from": {
                    "component": "IDP Credential",
                    "socketName": "AWS Credential",
                },
                "to": "AWS Credential",
            },
            {
                "from": {
                    "component": "IDP - us-east-1",
                    "socketName": "Region",
                },
                "to": "Region",
            },
            {
                "from": {
                    "component": "idp-subnet-pub-1",
                    "socketName": "Subnet Id",
                },
                "to": "Subnet Id",
            },
        ],
        "viewName": "Rokket",
        "domain": {
            "ImageId": "ami-05ffe3c48a9991133",
            "InstanceType": "t3.micro",
            "UserData": "IyEvYmluL2Jhc2gKc2V0IC1ldXgKCiMgSW5zdGFsbCBjdXJsCmRuZiBpbnN0YWxsIC15IGN1cmwKCiMgSW5zdGFsbCBPbGxhbWEKY3VybCAtZnNTTCBodHRwczovL29sbGFtYS5jb20vaW5zdGFsbC5zaCB8IHNoCgojIEVuYWJsZSBPbGxhbWEgc3lzdGVtZCBzZXJ2aWNlIHRvIHN0YXJ0IG9uIGJvb3QKc3lzdGVtY3RsIGVuYWJsZSAtLW5vdyBvbGxhbWE=",
        },
    }
    api.create_component(component)

    return jsonify(
        {
            "status": "ok",
            "workspace": "https://app.systeminit.com/w/01JZ67D72Q4ZXTXKZG6DA1CVZ4/01JZ67DE98F8V8DMZDMPSEC23X/c",
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
