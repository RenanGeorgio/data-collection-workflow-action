import os
import sys
import logging
from obsei.configuration import ObseiConfiguration
from obsei.preprocessor.text_cleaner import TextCleaner, TextCleanerConfig
from obsei.preprocessor.text_cleaning_function import *
from obsei.sink.http_sink import HttpSink, HttpSinkConfig
from obsei.sink.elasticsearch_sink import ElasticSearchSink, ElasticSearchSinkConfig
from obsei.source.website_crawler_source import (
    TrafilaturaCrawlerConfig,
    TrafilaturaCrawlerSource,
)

# Read workflow config file
current_path = os.path.dirname(os.path.realpath(__file__))
filename = "workflow.yml"

obsei_configuration = ObseiConfiguration(
     config_path=current_path,
     config_filename=filename
)

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def print_list(response_list):
    for response in response_list:
        print(response.__dict__)

def getWebInfo():
     source_config = TrafilaturaCrawlerConfig(
          urls=["https://haystack.deepset.ai/"],
          #is_feed=True, # RSS feed
          is_sitemap=True # Full website
     )

     return source_config

def main():
     # Initialize Observer based on workflow
     source_config = getWebInfo()

     source = TrafilaturaCrawlerSource()

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
     print_list(cleaner_response_list)

     # Execute Analyzer to perform analysis on Observer's output with given analyzer config
     analyzer_response_list = analyzer.analyze_input(source_response_list= cleaner_response_list, analyzer_config=analyzer_config)

     #sink_config = ElasticSearchSinkConfig(
     #     host="localhost",
     #     port=9200,
     #     index_name="test",
     #)
     #sink = ElasticSearchSink()
     #sink_response = sink.send_data(analyzer_response_list, sink_config)
     
     # Send analyzed result to Informer
     sink_response_list = sink.send_data(analyzer_response_list, sink_config)


if __name__ == '__main__':
  main()