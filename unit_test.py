# encoding=utf8

import re
import sys
import json
import urllib.error
import urllib.parse
import urllib.request

API_BASEURL = "http://0.0.0.0:80"

def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


one_city_request = {
    "city": "Barnaul",
    "parameters": "temperature feels wind visibility humidity"
}

many_city_request = {
    "cities": ["Barnaul", "Moscow", "London"],
    "parameters": "temperature feels wind visibility humidity"
}


def test_one_city():

    status, _ = request("/city_weather", method="GET", data=one_city_request)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test one city weather passed.")


def test_many_city():

    status, _ = request("/cities_weather", method="GET", data=many_city_request)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test many city weather passed.")

one_not_found_city_request = {
    "city": "dfgdf",
    "parameters": "temperature feels wind visibility humidity"
}

def test_not_found_city():

    status, _ = request("/city_weather", method="GET", data=one_not_found_city_request)

    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test not found city weather passed.")

def test_all():
    test_one_city()
    test_many_city()
    test_not_found_city()


def main():
    global API_BASEURL
    test_name = None

    for arg in sys.argv[1:]:
        if re.match(r"^https?://", arg):
            API_BASEURL = arg
        elif test_name is None:
            test_name = arg

    if API_BASEURL.endswith('/'):
        API_BASEURL = API_BASEURL[:-1]

    print(f"Testing API on {API_BASEURL}")

    if test_name is None:
        test_all()
    else:
        test_func = globals().get(f"test_{test_name}")
        if not test_func:
            print(f"Unknown test: {test_name}")
            sys.exit(1)
        test_func()


if __name__ == "__main__":
    main()
