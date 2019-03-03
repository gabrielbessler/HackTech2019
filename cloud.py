# Import the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import pickle
'''
# Load the text string
with open('test.txt', 'r') as f:
        text = f.read()
'''
class CloudConnect:
        def __init__(self):
                # Instantiate a client
                self.client = language.LanguageServiceClient()


        def get_entities(self, text):
                # Craft a document object
                document = types.Document(
                        content=text,
                        type=enums.Document.Type.PLAIN_TEXT
                )
                
                # Use the client to send it and receive a response
                response = self.client.analyze_entities(
                        document=document,
                        encoding_type='UTF32'
                )
                
                return response

        def process_entities_response(self, response):
                '''Take a response and return the relevant entities we care about,
                their offset, and their wikipedia links.'''
                results = []
                for entity in response.entities:
                        name = entity.name
                        Type = enums.Entity.Type(entity.type).name
                        metadata = entity.metadata
                        salience = entity.salience
                        metadata_entries = set(metadata.keys())
                        mentions = entity.mentions
                        if 'wikipedia_url' in metadata_entries:
                                url = metadata['wikipedia_url']
                                results.append((name, mentions, url, Type))
                return results
        
        def get_syntax(self, text):
                # Craft a document object
                document = types.Document(
                        content=text,
                        type=enums.Document.Type.PLAIN_TEXT
                )
                
                # Use the client to send it and receive a response
                response = self.client.analyze_syntax(
                        document=document,
                        encoding_type='UTF32'
                )
                
                return response
cloud = CloudConnect()
