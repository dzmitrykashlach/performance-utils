import json
import sys

import regex
import requests
from datetime import date
import time
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# configuration
BASE_URL = r'https://wiki-stag.wdf.sap.corp/wiki'
SEARCH_URL: str = BASE_URL + r'/rest/api/search?cql=siteSearch~%%22%s%%22'
EXPAIN_SEARCH_URL: str = BASE_URL + r'/explain.action?queryString=%%22%s%%22'
JSESSIONID: str = r'JSESSIONID=30A23BC1CE723A5096F3225ADB3CCC4B'

# request settings
CONTENT_TYPE_PARAM: str = r'Content-Type'
APPLICATION_JSON_PARAM: str = r'application/json'
COOKIE_PARAM: str = r'Cookie'

# output data
OUTPUT_DIRECTORY: str = r'output/contentbody.maxsize.default/'
# OUTPUT_DIRECTORY: str = r'output/contentbody.maxsize...MB/'

# configuration data params
EMPTY_PARAM = r''
NEW_LINE_DATA_PARAM: str = "\n"
FILENAME_DELIMITER: str = r'-'


# read spaces from data.txt
def load_search_queries():
    search_queries_path: str = sys.argv[1] if len(sys.argv) > 1 else r'search-terms-swa-prod-06.2021-20.txt'

    # load original spaces
    with open(search_queries_path, encoding="utf-8") as params:
        search_queries = params.read().splitlines()

    return search_queries


def make_explain_json(response_text):
    explain_dict = {}
    ranks = regex.findall(r"\((\d{1,2})\)\s{1}(.+)<", response_text)
    scores = regex.findall(r"strong>:\n(\d+\.{1}\d+)", response_text)
    for r in ranks:
        ri = ranks.index(r)
        explain_dict[r[1]] = [int(r[0]), float(scores[ri]) / 100]
    return json.dumps(explain_dict)


class SearchRelevanceTestingUtils(object):

    def __init__(self):
        # statistics params
        self.__number_of_search_queries = 0
        self.__number_of_errors = 0
        self.__waiting_time = 3

        # configuration params
        self.__init_global_configuration()

        # cql search params
        self.__search_queries_statistics = []

    # init global configuration
    def __init_global_configuration(self):
        self.__headers = {
            CONTENT_TYPE_PARAM: APPLICATION_JSON_PARAM,
            COOKIE_PARAM: JSESSIONID
        }
        self.__search_queries = load_search_queries()

    # run cql search for each space
    def run_search_testing(self):
        time_start = time.time()
        for i, search_query in enumerate(reversed(self.__search_queries), start=1):
            print("Run %s. Trying to check '%s' search query..." % (i, search_query))
            url = SEARCH_URL % search_query
            response = self.__send_get_request(url)
            self.__print_response_details(response, search_query)
            print("Trying to check '%s' explain query...\n" % (search_query))
            url = EXPAIN_SEARCH_URL % search_query
            response = self.__send_get_request(url)
            self.__parse_explain_details(response)
            self.__number_of_search_queries = self.__number_of_search_queries + 1
            self.__save_data(search_query, NEW_LINE_DATA_PARAM, self.__search_queries_statistics)
            self.__search_queries_statistics = []
        time_finish = time.time()
        total_time = round(time_finish - time_start, 3)
        self.__print_general_statistics(total_time)

    # run cql search for single space
    def __send_get_request(self, url):
        try:
            response = requests.get(url, headers=self.__headers, verify=False)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_error:
            self.__sleep_on_http_error("HTTP error", http_error)
        except requests.exceptions.ConnectionError as connection_error:
            self.__sleep_on_http_error("Connection error", connection_error, seconds=120)
        except requests.exceptions.Timeout as timeout_error:
            self.__sleep_on_http_error("Timeout error", timeout_error, seconds=120)
        except requests.exceptions.RequestException as request_error:
            self.__sleep_on_http_error("Unexpected error", request_error, seconds=30)
        self.__sleep(0)

    def __sleep(self, seconds):
        print("Sleep %s sec...\n" % seconds)
        time.sleep(seconds)
        self.__waiting_time = self.__waiting_time + seconds

    # sleep if request error was caught
    def __sleep_on_http_error(self, error_type, error, seconds=None):
        print("%s: " % error_type, error)
        if seconds is not None:
            minutes = seconds // 60
            print("Sleep %s min..." % str(minutes))
            time.sleep(seconds)
        self.__number_of_errors = self.__number_of_errors + 1

    # print the statistics of cql search for single space
    def __print_response_details(self, response, search_query):
        print("The result of search query '%s' testing:" % search_query)
        print("\t- status code: %s;" % str(response.status_code))

        if response.ok:
            response_json = response.json()
            if response_json["totalSize"] and response_json["searchDuration"]:
                self.__search_queries_statistics.append(response_json["searchDuration"])

    # print the statistics of cql search for single space
    def __parse_explain_details(self, response):
        print("\t- status code: %s;" % str(response.status_code))
        if response.ok:
            response_text = response.text
            explain_dict_json = make_explain_json(response_text)
            self.__search_queries_statistics.append(explain_dict_json)
            self.__search_queries_statistics.append(NEW_LINE_DATA_PARAM)

    def __print_general_statistics(self, total_time):

        # save statistics for CQL search queries

        print("\nTotal time: %s sec, where `waiting time`: %s sec." % (total_time, self.__waiting_time))
        print(
            "Number of all search queries: %s from %s." % (self.__number_of_search_queries, len(self.__search_queries)))
        print("Number of errors: %s." % self.__number_of_errors)

    @staticmethod
    def __save_data(filename, data_param, data):
        filename = OUTPUT_DIRECTORY + filename
        with open(filename, "w+") as outfile:
            outfile.write(data_param.join(str(data_element) for data_element in data))
        print("\nThe result can be found at '%s'." % filename)


search_relevance_testing: SearchRelevanceTestingUtils = SearchRelevanceTestingUtils()
search_relevance_testing.run_search_testing()
