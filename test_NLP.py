from google.cloud import language_v1
import os
import io
import json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''

def analyze_nlp(text_content):

    client = language_v1.LanguageServiceClient()
    
    type_ = language_v1.Document.Type.PLAIN_TEXT
    
    language = "en"
    
    document = {"content": text_content, "type_": type_, "language": language}
    
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    nlp = {
        "sentiment_score": "",
        "sentiment_magnitude": "",
        "sentiment": ""
    }

    nlp["sentiment_score"] = response.document_sentiment.score
    nlp["sentiment_magnitude"] = response.document_sentiment.magnitude
    
    if response.document_sentiment.score < 0:
        nlp["sentiment"] = "negative"
    elif response.document_sentiment.score > 0:
        nlp["sentiment"] = "positive"
    else:
        nlp["neutral"] = "neutral"

    return json.dumps(nlp)

if __name__ == "__main__":
    print("Text that you want to NLP analyze: ")
    text = input()
    print(analyze_nlp(text))