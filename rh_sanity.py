#! /usr/bin/python3
import requests

from argparse import ArgumentParser

RH_URL = 'releasehub-staging.cloud.chippercash.com'

class HTTPCall:

    def __init__(self):
        pass

    def get(self, url):
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp

    def post(self, url, data):
        resp = requests.post(url, data=data, timeout=5)
        resp.raise_for_status()
        return resp

    def data(self, resp):
        return resp.json()



def core(handle):
    url = f'https://core-{handle}.{RH_URL}/v1/public/health'
    obj = HTTPCall()
    resp = obj.get(url)
    return obj.data(resp)


def auth(handle, email):
    # Part 1
    obj = HTTPCall()
    url = f'https://auth-{handle}.{RH_URL}/otp/email'    
    data_otp = {'emailAddress': email}

    # Part 2
    if obj.post(url, data_otp).status_code == 200:
        url = f'https://auth-{handle}.{RH_URL}/jwt?otp=111111'
        data = {'identifier': email, 'otpType': 'EMAIL'}
        resp = obj.post(url, data)
        return obj.data(resp)


def comp():
    pass



if __name__ == "__main__":
    # TODO: add Postgres checks AFTER fixing network accessibility

    # Read arguments
    parser = ArgumentParser(description='ReleaseHub environment handle tests', add_help=True)
    required = parser.add_argument_group('required arguments')
    required.add_argument('--handle', '-a', dest='handle', help='input env handle', required=True)
    required.add_argument('--email', '-e', dest='email', help='input email for auth', required=True)
    args = parser.parse_args()

    # All relevant to establish env 'complete'
    apps = ['core', 'auth', 'comp']

    # Wrap all in try block and exit on 1st failure
    try:
        data = core(args.handle)
        print(f"Response from core: {data}")
        data = auth(args.handle, args.email)
        print(f"Response from auth: {data}")
    except Exception as e:
        print(e)
        exit(1)
