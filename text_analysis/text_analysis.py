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

import requests

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features,EntitiesOptions,KeywordsOptions
# [END text_analysis imports]

# GLOBAL VARIABLES
naturalLanguageUnderstanding = NaturalLanguageUnderstandingV1(
                                                              version='2018-11-16',
                                        iam_apikey='Jk2q3V3rmzrGTYtlp4tCZ8sTmQ2S8fkwZCyjn5LnvPPz',
                                                              url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-11-16')

def get_total_tone():
    filename = "all_sentences.txt"
    file_sentences = open(filename,"r")
    #data = json.loads(file_sentences)
    data = file_sentences.read()
    print(data)
    response = naturalLanguageUnderstanding.analyze(
                                                text=data,
                                                features=Features(
                                                        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                                                        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                                        limit=2)),language='en').get_result()
    return response

def get_IBM_tone(sentence):
    response = naturalLanguageUnderstanding.analyze(
                                                text=sentence,
                                                features=Features(
                                                            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                                                            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                                            limit=2)),language='en').get_result()
#print(json.dumps(response, indent=2))
    return response

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

# [START text_analysis run app]
def main():
    filenameAllSentences = "all_sentences.txt"
#    key = 0
#    print("Press 's' to speak.")

#    while(key!='q'):
#        key = click.getchar()
#        if(key=='s'):
#            print("You may speak.\n")
    sentence = mic_speech.main()
    
    #Get analysis results
    entities_result = analyze_entities(sentence, get_native_encoding_type())
    sentiment_result = analyze_sentiment(sentence, get_native_encoding_type())
    syntax_result = analyze_syntax(sentence, get_native_encoding_type())
    tone_result = get_IBM_tone(sentence)
    
    #Add to total sentences
    fileTotal = open(filenameAllSentences,"a+")
    fileTotal.write(sentence+" ")
    fileTotal.close()
    
    total_tone_result = get_total_tone()
 
    #Dump json results
    filename = ("sentenceInfo.json")
    fileInfo = open(filename,"w")
    fileInfo.write("{ \"entries\":")
    fileInfo.write(json.dumps(entities_result, indent=2))
    fileInfo.write(",\"sentiment\":")
    fileInfo.write(json.dumps(sentiment_result, indent=2))
    fileInfo.write(",\"syntax\":")
    fileInfo.write(json.dumps(syntax_result, indent=2))
    fileInfo.write(",\"tone\":")
    fileInfo.write(json.dumps(tone_result, indent=2))
    fileInfo.write(",\"total_tone\":")
    fileInfo.write(json.dumps(total_tone_result, indent=2))
    fileInfo.write("}")
    fileInfo.close()
#            print("Press 's' to speak again or Press 'q' to quit.")

# [START text_analysis run app]
if __name__ == '__main__':
    main()

# [END text_analysis run app]
# [END text_analysis]
