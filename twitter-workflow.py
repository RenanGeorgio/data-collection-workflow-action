import os
import sys
import logging
from obsei.configuration import ObseiConfiguration
from obsei.preprocessor.text_cleaner import TextCleaner, TextCleanerConfig
from obsei.preprocessor.text_cleaning_function import *
from obsei.source.twitter_source import TwitterSourceConfig, TwitterSource, TwitterCredentials
from obsei.sink.http_sink import HttpSink, HttpSinkConfig
from obsei.sink.elasticsearch_sink import ElasticSearchSink, ElasticSearchSinkConfig

# Read workflow config file
current_path = os.path.dirname(os.path.realpath(__file__))
filename = "workflow.yml"

obsei_configuration = ObseiConfiguration(
     config_path=current_path,
     config_filename=filename
)

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

twitter_cred_info = None

# Enter your twitter credentials
# Get it from https://developer.twitter.com/en/apply-for-access
# Currently it will fetch from environment variables: twitter_bearer_token, twitter_consumer_key, twitter_consumer_secret
# Uncomment below lines if you like to pass credentials directly instead of env variables

# twitter_cred_info = TwitterCredentials(
#     bearer_token='<Enter bearer_token>',
#     consumer_key="<Enter consumer_key>",
#     consumer_secret="<Enter consumer_secret>"
# )

def getTreandTopic():
     source_config = TwitterSourceConfig(
          query="bitcoin",
          lookup_period="1h",
          tweet_fields=[
               "author_id",
               "conversation_id",
               "created_at",
               "id",
               "public_metrics",
               "text",
          ],
          user_fields=["id", "name", "public_metrics", "username", "verified"],
          expansions=["author_id"],
          place_fields=None,
          max_tweets=10,
          cred_info=twitter_cred_info or None
     )

     return source_config

def main():
     # Initialize Observer based on workflow
     source_config = getTreandTopic()

     source = TwitterSource()

     text_cleaner_config = TextCleanerConfig(
          cleaning_functions = [
               ToLowerCase(),
               RemoveWhiteSpaceAndEmptyToken(),
               RemovePunctuation(),
               RemoveSpecialChars(),
               DecodeUnicode(),
               RemoveStopWords(),
               RemoveWhiteSpaceAndEmptyToken(),
          ]
     )

     text_cleaner = TextCleaner()

     # Initialize Analyzer based on workflow
     analyzer = obsei_configuration.initialize_instance("analyzer")
     analyzer_config = obsei_configuration.initialize_instance("analyzer_config")

     # Initialize Informer based on workflow
     sink_config = obsei_configuration.initialize_instance("sink_config")
     sink = obsei_configuration.initialize_instance("sink")

     # Execute Observer to fetch result
     source_response_list = source.lookup(source_config)

     # PreProcess text to clean it
     cleaner_response_list = text_cleaner.preprocess_input(input_list=source_response_list, config=text_cleaner_config)

     # Execute Analyzer to perform analysis on Observer's output with given analyzer config
     analyzer_response_list = analyzer.analyze_input(source_response_list= cleaner_response_list, analyzer_config=analyzer_config)

     # Send analyzed result to Informer
     sink_response_list = sink.send_data(analyzer_response_list, sink_config)

     for idx, sink_response in enumerate(sink_response_list):
          logger.info(f"source_response#'{idx}'='{sink_response.__dict__}'")


if __name__ == '__main__':
  main()