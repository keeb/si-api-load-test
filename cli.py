#!/usr/bin/env python3

import sys
import requests
import time
from terminaltexteffects.effects import effect_rain

API_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiMiIsInVzZXJJZCI6IjAxSEFBUjJYQUtNWVZQQzhFWkNDUlJDVlNRIiwid29ya3NwYWNlSWQiOiIwMUpRUEtaUThLWDlRNE5ZNzdNMlBRQTA2RSIsInJvbGUiOiJhdXRvbWF0aW9uIiwiaWF0IjoxNzQzNDQyOTI0LCJleHAiOjE3NzUwMDA1MjQsInN1YiI6IjAxSEFBUjJYQUtNWVZQQzhFWkNDUlJDVlNRIiwianRpIjoiMDFKUVBNUU1UUFQ1WDAwOVBYOTFEQ1NERFkifQ.W96J1rivVV0zlyJjsytXhWchIwpLduwhfHp4UAYsGH2us6mH2ckh8wPYBgC2LU9Fj40phiMayqa23Kxx5Cv2I9x4I2qHv20BDqjSir5s4eBHXIhCVdLzDCgae-_DQ9UZDU3doPgH-4Udjffc1nrV7_U177fMKvkehnS2HyUqqdvIeL2a6XdEy4oRQJ3jHFuZmvhNru5bZePtBNuO1I6ii4iRkcURCqveSkzxTefL9S6U-6VVV2kHv5vdD6DeBW5jC7PEvB4Sfed9FEIYjdckptJPBgpWfkAP6q92WdknePpi7Uw7kPP0QlmQbwG5CTDKCmF5QPMLd6UCpUHARnrrCfX1aCjLJZrDd3gQuh75S8xY02g2DB8vGEE_ShNHsu-d_zgJaRoXep4ItrIjyp1899rx8QxtWb4bKB6zUqP1TKxRvAokOjuGyGFBuQD18-XsC2yxwp7ewA7Jxf8X27nk6QrtYrJqOZDgLJXKmkobqQo73Ed0lBWEaUjGNSmWTpqsuC29S4po-FTuJeYtAg5-jDjmQ4ByNzWX-ZY0bIgBuMImrXxnf88q2rkkDHNETacuJ_tCErWlzy1bfTb9jnHleGmCiHx0rP4JGgUlqoq9OzVZbU126WlRykfnoBWoJi62l1tOdUHjMFzMXFcSEq1HQH1seAnDEmgso0C_K6f0flQ"
API_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiMiIsInVzZXJJZCI6IjAxSEFBUjJYQUtNWVZQQzhFWkNDUlJDVlNRIiwid29ya3NwYWNlSWQiOiIwMUpUNDRCV1pHQUdSRVhRNjhHVlBaU0s3VCIsInJvbGUiOiJhdXRvbWF0aW9uIiwiaWF0IjoxNzQ3NDEwMTU1LCJleHAiOjE3NTAwMDIxNTUsInN1YiI6IjAxSEFBUjJYQUtNWVZQQzhFWkNDUlJDVlNRIiwianRpIjoiMDFKVkNXNVk3Tk5STTQ0NzFYSzlHNloyU0YifQ.Gc38mZuNuUcLyjvmv7u_SZeOGQ7_ZT5q_A0KmZePqJkWoX_trRn15pGhoHPVtkXXriVDTfV-9TK62xVG-WJjSpbcyptdxQutEh6IZy0XjY8WTFPJtPB0zVTk-f13f1EAyynOigqs1l7ZrSW-Qh0nJusCy7-dxQMr3NTQxFUqcjn1-3ngPDfQPIBTFSV7uVd6yTbFR7tjyWjlP5OaFam4b-lMz2GVlcjZyCeDCAYu9Rt81riiUn3RQ5vLlZlE6QhxCn7t3NlgkzrfFz6kngjSBAi5GkENKYHriTj6uoVI0cZ9SiAa3gTF0gXvc1R3-CNh3FWKP-jfLNW-U2NM3mBk6fS7EbRu6grRnu5WTLjgk9fBhsHCrY6tcf0D-briCbynXpCCnPWu058W_Tlf7rfEZPQQeSFbsG57_N1H6iXrjk5MDg4n-oXCPx19yDQC-4NqPl584wguLF6mFdq9nyoN9vzdVg1rRGDb_uaCDoQzQb3b1vmgjksCVQOvNQeJ258vghdzv63eTprRTFT0cUmM8tDceFgxx5ATrr7O_XfaZl9QsCGUrYmCj75_-YVR2jUYXwGVZWvC2Z-etCotk5Qogz2-JOig6dWPrd3wkt0yHgEEVtArGtZUkzwcRJHDRUlUuPC_Q-sWXMttN2DKqXeYQmips5VVl_X-rup3ZJK2cos"
# si.keeb.dev
API_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiMiIsInVzZXJJZCI6IjAxSEFBUjJYQUtNWVZQQzhFWkNDUlJDVlNRIiwid29ya3NwYWNlSWQiOiIwMUhLRzdOQ0dWV0JQREMxNjEwMjc5ODU4ViIsInJvbGUiOiJhdXRvbWF0aW9uIiwiaWF0IjoxNzQ3OTM1Njk2LCJleHAiOjE3Nzk0OTMyOTYsInN1YiI6IjAxSEFBUjJYQUtNWVZQQzhFWkNDUlJDVlNRIiwianRpIjoiMDFKVldIQzVNTU5NSzRXUUtFVEEyQzcyRFgifQ.NBD4jR0jTa3HeeXjY4gU06tlo1qXTN_S9z24iYJp1DBPWJLQXzPepu7cAmeYhLnXXB9EViu_w1sup3PIyZr_YRSffJE4_QXGtAqyvTxrLO7Ic4SunGNRNLXalh7SxwwJcP4HqOFe5pJG1M9eabkApuzvtAr85NObwOGO_dozVarr-56Clb8M4rXaMv-O2TqKgpWC4UUPJ166vN2jrxZ73RfWcf3CXAQUuTOjgxbfRTJA8kRz3Fqeu2fLGfD9ockDLhHr-BtIqQ-KwOkxSVPHRm7i_9InNX_VIqyskCHhb1tTApBQ29O3CVdz5upWJAFdioI7WdIVEyXKfAXwftt0pV85_aT-Uu1mBca-kYzzGGuXM-87CZDfnCwCn_uWyYeOaDmBoQQF6avtu89_IKkpyLW2p_14kqMaB1mwq5t37tW5q2kHO6qTxL4Fa3Jr58Nxfb3zEhH1hcA5fD3-CSH4ILljRPHJoC3CNpzzBnXU3mEUis7ISZ8F7nPSsu-TTFKvWkH1Gff1i731qcMEA-wn9-AdhSLNoCJHmAe05IlcLFcq13YxAqvhnIXTeIgCH0hc9QXtTrBd5iZk7jCtfsC3Sx82ct-FPilDdj7M27LOLBaR9AsikLqWYCHM5heOocbePE0jfVtvccI19z-B4acdXmWIidMB-XfXE3tzQCKV6Ps"

BASE_URL =  "https://api.systeminit.com/"
BASE_URL =  "http://jack:5380"


with open("logo") as f:
    text = "".join(f.readlines())
    effect = effect_rain.Rain(text)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

class Session:
    def __init__(self, user_id=None, user_email=None, workspace_id=None, role=None):
        self.user_id = user_id
        self.user_email = user_email
        self.workspace_id = workspace_id
        self.change_set_id = None
        self.role = role

    @classmethod
    def from_ret(cls, ret):
        if ret.ok:
            data = ret.json()
            return cls(
                user_id=data["userId"],
                user_email=data["userEmail"],
                workspace_id=data["workspaceId"],
                role=data["token"]["role"]
            )
        else:
            return None
        
    def __str__(self):
        return f"User ID: {self.user_id}\nUser Email: {self.user_email}\nWorkspace ID: {self.workspace_id}\nRole: {self.role}"

ret = requests.get(f"{BASE_URL}/whoami", headers=headers)
session_data = Session.from_ret(ret)
workspace_id = session_data.workspace_id


def whoami():
    return session_data

def create_change_set(name):
    post_data = {"changeSetName": name}
    data = requests.post(f"{BASE_URL}/v1/w/{workspace_id}/change-sets", headers=headers, json=post_data)
    change_set_data = data.json()
    change_set_id = change_set_data["changeSet"]["id"]
    session_data.change_set_id = change_set_id

def get_change_sets():
    data = requests.get(f"{BASE_URL}/v1/w/{workspace_id}/change-sets", headers=headers)
    return data.json()

def delete_change_set(id):
    data = requests.delete(f"{BASE_URL}/v1/w/{workspace_id}/change-sets/{id}", headers=headers)




def create_account():
    print (f"creating component Account Creator")
def create_network():
    print (f"creating component VPC Creator")

def create_application():
    print (f"creating component Standard VPC Application")
    print (f"setting values")


def delete_all_changesets():
    change_sets = get_change_sets()
    len_change_sets = len(change_sets["changeSets"])
    print(f"number of starting change sets {len_change_sets}" )
    for change in change_sets["changeSets"]:
        id = change["id"]
        delete_change_set(id)
    change_sets = get_change_sets()
    len_change_sets = len(change_sets["changeSets"])
    print(f"number of remaining change sets {len_change_sets}" )    



def process_message(message):
    command = message.split(" ")[0]
    args = " ".join(message.split(" ")[1:])

    if command == "exit":
        exit()
    elif command == "init":
        print(f"creating workspace {args}")
        return "https://app.systeminit.com/w/01JQPKZQ8KX9Q4NY77M2PQA06E/head/c"
    
    elif command == "change_set":
        create_change_set(args)
        print (f"created change set {args}")
        return f"change set id: {session_data.change_set_id}"
    elif command == "run":
        return f"running management function {args}"
    elif command == "whoami":
        return whoami()
    elif command == "login":
        return whoami()
    elif command == "create_account":
        create_account()
    elif command == "create_network":
        create_network()
    elif command == "create_application":
        create_application()
    elif command == "deploy":
        create_change_set("deploy")
        create_account()
        create_network()
        create_application()
        print( f"deploying application {args} ..." )
        print ("running Account Creator management function ...")
        time.sleep(0.3)
        print ("running VPC Creator management function ...")
        time.sleep(0.3)
        print ("running Standard VPC Application management function ...")
        time.sleep(0.3)
        print ("Workspace is now ready to DEPLOY")
        time.sleep(0.3)
        print ("https://app.systeminit.com/w/01JPZQDTT9V6XR99ES8TDGWK90/01JPZS531T7TK1TDXY3EHTQ7DP/c/01JPZQREW4YNXK4RN8T3V5FHJA/v/")
        return ""
    elif command == "destroy":
        delete_all_changesets()
        return "DOOM!"


def exit():
    sys.exit(0)



while True:
    text = input("> ")
    print(process_message(text))
