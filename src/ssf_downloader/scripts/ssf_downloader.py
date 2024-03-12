import os
import json
import asyncio
import argparse
from ssf_downloader.models import UserInfo
from ssf_downloader.client import SSFClient

def get_args():
    parser = argparse.ArgumentParser(prog='ssf_downloader')
    subparsers = parser.add_subparsers(dest='subparser')

    register_parser = subparsers.add_parser('register')
    register_parser.add_argument(
        '-u',
        '--username',
        dest='username',
        help='Your username',
        required=True
    )
    register_parser.add_argument(
        '-e',
        '--email',
        dest='email',
        help='Your email',
        required=True
    )
    register_parser.add_argument(
        '-p',
        '--password',
        dest='password',
        help='Your password',
        required=True
    )

    login_parser = subparsers.add_parser('login')
    login_parser.add_argument(
        '-u',
        '--username',
        dest='username',
        help='Your 77file.com account username',
        required=True
    )
    login_parser.add_argument(
        '-p',
        '--password',
        dest='password',
        help='Your 77file.com account password',
        required=True
    )

    get_file_info_parser = subparsers.add_parser('get_file')
    get_file_info_parser.add_argument(
        '-url',
        dest='url',
        help='77file.com url',
        required=True
    )
    
    return parser.parse_args()

def save_session(client, filename='session.json'):
    session = dict(
        username=client.username,
        password=client.password,
        device_id=client.device_id,
        user_info=client.user_info.dict()
    )
    json_string = json.dumps(session, indent=4)

    with open(filename, 'w') as file_handler:
        file_handler.write(json_string)

def load_session(client, filename='session.json'):
    with open(filename, 'r') as file_handler:
        json_string = json.load(file_handler)

    client.username  = json_string['username']
    client.password  = json_string['password']
    client.device_id = json_string['device_id']
    client.user_info = UserInfo(**json_string['user_info'])

async def register(client, username, email, password):
    await client.register(username, email, password)

async def login(client, username, password):
    await client.login(username, password)
    save_session(client)

async def get_file(client, url):
    if 'session.json' not in os.listdir():
        raise FileNotFoundError('`session.json` not found, please login first!')

    load_session(client)
    result = (await client.get_file_details(url)).json()
    print(result)
    
async def run():
    args = get_args()
    async with SSFClient() as client:
        if args.subparser == 'register':
            await register(
                client,
                args.username,
                args.email,
                args.password
            )
        elif args.subparser == 'login':
            await login(
                client,
                args.username,
                args.password
            )
        elif args.subparser == 'get_file':
            await get_file(
                client,
                args.url
            )
        else:
            raise ValueError('invalid command')

def main():
    asyncio.run(run())