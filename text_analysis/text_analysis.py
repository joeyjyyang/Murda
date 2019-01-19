# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START text_analysis]
"""Takes speech, converts to text and performs text analysis."""

import sys
import json

# [START text_analysis imports]
import mic_speech
import click

import googleapiclient.discovery
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
# [END text_analysis imports]

# GLOBAL VARIABLES
numSentences=0

def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'

def analyze_entities(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding,
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeEntities(body=body)
    response = request.execute()

    return response

def analyze_sentiment(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()

    return response

def analyze_syntax(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSyntax(body=body)
    response = request.execute()

    return response

def analyze(content):
    # [START language_sentiment_text_core]
    
    client = language_v1.LanguageServiceClient()
    
    # content = 'Your text to analyze, e.g. Hello, world!'
    
    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')
    
    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))

    # [END language_sentiment_text_core]

# [START text_analysis run app]
if __name__ == '__main__':
    filenameAllSentences = "all_sentences.txt"
    fileTotal = open(filenameAllSentences,"w")
    fileTotal.close()
    numSentences = 0
    key = 0
    print("Press 's' to speak.")

    while(key!='q'):
        key = click.getchar()
        if(key=='s'):
            print("You may speak.\n")
            sentence = mic_speech.main()
            numSentences += 1
            
            entities_result = analyze_entities(sentence, get_native_encoding_type())
            sentiment_result = analyze_sentiment(sentence, get_native_encoding_type())
            syntax_result = analyze_syntax(sentence, get_native_encoding_type())
            
            fileTotal = open(filenameAllSentences,"a+")
            fileTotal.write(sentence)
            fileTotal.close()

            filename = ("sentenceInfo.json")
            fileInfo = open(filename,"w")
            fileInfo.write(json.dumps(entities_result, indent=2))
            fileInfo.write(json.dumps(sentiment_result, indent=2))
            fileInfo.write(json.dumps(syntax_result, indent=2))
            fileInfo.close()
            print("Press 's' to speak again or Press 'q' to quit.")

# [END text_analysis run app]
# [END text_analysis]
