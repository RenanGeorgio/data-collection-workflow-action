import os
import sys
import time
import logging
from obsei.workflow.store import WorkflowStore
from obsei.configuration import ObseiConfiguration
from obsei.workflow.workflow import Workflow, WorkflowConfig
from obsei.preprocessor.text_cleaner import TextCleaner, TextCleanerConfig
from obsei.preprocessor.text_cleaning_function import *
from obsei.source.google_news_source import GoogleNewsConfig, GoogleNewsSource
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

store = WorkflowStore()

def getNews():
     source_config = GoogleNewsConfig(
          query="bitcoin",
          country="BR",
          language="pt-br",
          max_results=10,
          fetch_article=True,
          lookup_period="1d"
          #crawler_config=None,
          #proxy="http://127.0.0.1:8080"
     )

     return source_config

def main():
     # Initialize Observer based on workflow
     source_config = getNews()

     # Create instance of workflow, adding observer config to it, it will autgenerate unique workflow id
     workflow = Workflow(config=WorkflowConfig(source_config=source_config))

     source = GoogleNewsSource(store=store)

     # Insert workflow config to DB store
     store.add_workflow(workflow)

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

     #sink_config = HttpSinkConfig(
     #     url="https://localhost:8080/api/path",
     #     headers={
     #          "Content-type": "application/json",
     #          "authorization": "Bearer " + os.environ["SUPPLYFY_TOKEN"]
     #     }
     #)

     #sink = HttpSink()

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
     analyzer_response_list = analyzer.analyze_input(source_response_list=cleaner_response_list, analyzer_config=analyzer_config)

     # Send analyzed result to Informer
     sink_response_list = sink.send_data(analyzer_response_list, sink_config)


if __name__ == '__main__':
  main()