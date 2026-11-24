"""Tools shared by the check.py files of lab 2. You do not need to change (or even read) this file.

check.py tests your functions WITHOUT the internet: instead of a real requests.Session, it gives them a
FakeSession that answers with the files saved in samples/ and remembers every request you made.
"""
import json
import sys

sys.stdout.reconfigure(errors="replace")       # a character the terminal cannot show becomes "?", not an error

results = {"ok": 0, "fail": 0, "todo": 0}


def check(exercise, name, function, expected):
    """Run function(); compare with expected (a value, or a function that returns True/False)."""
    try:
        got = function()
    except NotImplementedError:
        results["todo"] += 1
        print(f"  ⬜ exercise {exercise}: {name}: not done yet")
        return
    except Exception as error:
        results["fail"] += 1
        print(f"  ❌ exercise {exercise}: {name}: error {error!r}")
        return
    good = expected(got) if callable(expected) else got == expected
    results["ok" if good else "fail"] += 1
    print(f"  {'✅' if good else '❌'} exercise {exercise}: {name}" + ("" if good else f"\n       got:      {got!r}"
          + ("" if callable(expected) else f"\n       expected: {expected!r}")))


def summary():
    print(f"\n{results['ok']} ✅   {results['fail']} ❌   {results['todo']} ⬜")
    if results["fail"] == 0 and results["todo"] == 0:
        print("All done. Now run the real thing: click Run ▶ on main.py")


class FakeResponse:
    """Looks like a requests.Response: status_code, headers, text, content, json(), raise_for_status(), iter_content()."""

    def __init__(self, status_code=200, json_data=None, text=None, content=None, headers=None, url=""):
        self.status_code = status_code
        self._json = json_data
        if content is None:
            content = (text if text is not None else json.dumps(json_data or {})).encode("utf-8")
        self.content = content
        self.text = text if text is not None else content.decode("utf-8", "replace")
        self.headers = headers or {}
        self.url = url
        self.ok = status_code < 400

    def json(self):
        if self._json is None:
            return json.loads(self.text)
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError(f"{self.status_code} Error for url: {self.url}", response=self)

    def iter_content(self, chunk_size=1024):
        for start in range(0, len(self.content), chunk_size):
            yield self.content[start:start + chunk_size]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def close(self):
        pass


class FakeSession:
    """Looks like a requests.Session. answer(method, url, params, kwargs) returns a FakeResponse.

    Every call is saved in .calls as a dict: method, url, params, kwargs.
    """

    def __init__(self, answer):
        self.answer = answer
        self.calls = []
        self.headers = {}

    def request(self, method, url, params=None, **kwargs):
        self.calls.append({"method": method, "url": url, "params": dict(params or {}), "kwargs": kwargs})
        response = self.answer(method, url, dict(params or {}), kwargs)
        response.url = response.url or url
        return response

    def get(self, url, params=None, **kwargs):
        return self.request("GET", url, params=params, **kwargs)

    def post(self, url, params=None, **kwargs):
        return self.request("POST", url, params=params, **kwargs)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
