import json
import os
import discord
import asyncio
import concurrent.futures
import threading
import time


class Utils:
    client = None
    # TODO: THIS IS SCUFFED AS HELL BUT I JUST WANT IT TO WORK
    pool = concurrent.futures.ThreadPoolExecutor()

    channel = None
    message = ""
    new_message = False
    send_buf = ""
    ready_to_send = False

    def get_user_input(self):
        # Flush message buffer and send it
        Utils.ready_to_send = True
        while not Utils.new_message:
            time.sleep(1)
        Utils.new_message = False
        msg = Utils.message
        # print(msg)
        return msg

def display_print(message):
    Utils.send_buf = Utils.send_buf + message + "\n"
    # print(Utils.send_buf)
    # print(message)

def get_user_input():
    command = input()
    # pre processing
    command.strip()
    command.lower()
    return command


def read_json(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    real_path = os.path.join(dir_path, path)
    data = []
    with open(real_path, 'r') as f:
        data = json.load(f)

    return data
