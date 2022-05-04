#! /usr/bin/python3
import requests

from argparse import ArgumentParser


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

    def status(self, resp):
        return resp.status_code


def core(handle):
    url = f'https://core-{handle}.releasehub-staging.cloud.chippercash.com/v1/public/health'
    obj = HTTPCall()
    resp = obj.get(url)
    return obj.data(resp)


def auth(handle, email):
    # Part 1
    obj = HTTPCall()
    url = f'https://auth-{handle}.releasehub-staging.cloud.chippercash.com/otp/email'    
    data_otp = {'emailAddress': email}

    # Part 2
    if obj.post(url, data_otp) == 200:
        url = f'https://auth-{handle}.releasehub-staging.cloud.chippercash.com/jwt?otp=111111'
        data = {'identifier': email, 'otpType': 'EMAIL'}
        resp = obj.post(url, data)
        return obj.data(resp)


def comp():
    pass



if __name__ == "__main__":
    # Steps:
    #     1)hit RH endpoint
    #     2)send otp email
    #     3)process response
    #     4)forward response to next/final POST
    # TODO: add Postgres checks AFTER fixing network accessibility

    # Read RH environment handle
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
