import requests

def bingsearchAPI(stringArray):
    phrase_string = stringArray
    # for i in stringArray:
    #     phrase_string = phrase_string + i + " "
    subscription_key = "e478d9f870454cc1b3f9619551688ce9"
    search_term = phrase_string
    search_url = "https://acrosstheaisle-bingsearchapi.cognitiveservices.azure.com/bing/v7.0/news/search"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results
