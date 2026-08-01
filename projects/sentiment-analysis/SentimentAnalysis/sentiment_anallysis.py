import requests, json


# define function that takes a string input (text_to_analyse)
def sentiment_analyzer(text_to_analyse):
    # URL of sentiment analysis service
    url = "https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict"

    # create dictionary with text to be analyzed
    myobj = {"raw_document": {"text": text_to_analyse}}

    # set headers required for the API request
    header = {
        "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
    }

    # send POST request to API with text and headers
    response = requests.post(url, json=myobj, headers=header)

    # if status code is 200
    if response.status_code == 200:
        # parse JSON response from API
        formatted_response = json.loads(response.text)

        # extract sentiment label and score from response
        label = formatted_response["documentSentiment"]["label"]
        score = formatted_response["documentSentiment"]["score"]
    elif response.status_code == 500:
        label = None
        score = None
    else:
        label = None
        score = None

    # return dictionary with sentiment analysis results
    return {"label": label, "score": score}
