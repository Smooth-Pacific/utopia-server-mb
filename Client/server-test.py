#!/usr/bin/env python3

# Creator: VPR
# Created: March 4th, 2022
# Updated: March 4th, 2022

# Notes:
#    Uses netcat

import os
import sys

from threading import Thread
from requests.auth import HTTPDigestAuth
from requests import (
    Session
)
#####################
## Setup variables ##
#####################

AUTH_USER="username1"
AUTH_PASS="password1"

HOST = "127.0.0.1" 
PORT = 8080

CERT_MEM="/usr/local/share/ca-certificates/smoothstack_root.crt"

####################
## Test functions ##
####################

def sendGetRequestToRoot() -> None:
    global n_passed, n_failed

    s = Session()
    s.auth = HTTPDigestAuth(username=AUTH_USER, password=AUTH_PASS)
    s.verify = CERT_MEM

    # Test "/" endpoint (root)
    resp = s.get(f"https://{HOST}:{PORT}/")
    s.close()

    if resp.status_code == 200:
        n_passed += 1
    else:
        n_failed += 1

if __name__ == "__main__":

    # Set global variables
    if os.environ.get("HOST"):
        HOST = os.environ.get("HOST")
    if os.environ.get("PORT"):
        PORT = os.environ.get("PORT")
    if os.environ.get("AUTH_USER"):
        AUTH_USER = os.environ.get("AUTH_USER")
    if os.environ.get("AUTH_PASS"):
        AUTH_PASS = os.environ.get("AUTH_PASS")
    if os.environ.get("CERT_MEM"):
        CERT_MEM = os.environ.get("CERT_MEM")

    # Check if server is running
    if os.system(f"nc -vz {HOST} {PORT}"):
        sys.stderr.write("Could not ping server...\n")
        sys.exit(1)

    # 100 iterations of digest authority stress testing
    n_passed, n_failed = 0, 0
    n_iterations = 25
    n_threads = 4
    for _ in range(n_iterations):
        threads = [ ]
        for _ in range(n_threads):
            threads.append(Thread(target=sendGetRequestToRoot))
            threads[-1].start()

        for thread in threads:
            thread.join()

    print(f"Passed: {n_passed}\nFailed: {n_failed}")
