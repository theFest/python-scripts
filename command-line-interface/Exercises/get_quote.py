import requests


def get_quote():
    url = "https://api.quotable.io/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['content']} - {data['author']}"
    else:
        return "Unable to retrieve a quote at this time."


print(get_quote())
