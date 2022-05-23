import csv
import filecmp
import json
import os
import numpy as np
from sklearn.metrics import dcg_score

OUTPUT = r'output'
BEFORE = r'before'
AFTER = r'after'
SEARCH_STATS_DIR = os.getcwd() + os.path.sep + OUTPUT + os.path.sep
CONTENTBODY_MAXSIZE = r"contentbody.maxsize"
BEFORE_DIR = SEARCH_STATS_DIR + r'contentbody.maxsize.default'
AFTER_DIR = SEARCH_STATS_DIR + r'contentbody.maxsize.MB'
CHART_DATA_FILE_CSV = "dcg.csv"


def load_search_term_file(filename):
    with open(filename) as f:
        content = [str.strip() for str in f]
        content.pop(2)
        content[1] = json.loads(content[1])
    return content


class SearchDataChartBuilder:
    def __init__(self):
        self.__chart_data = {}

    def calc_chart_data(self):
        # Check that number of files and filenames are equal in both directories
        dircmp = filecmp.dircmp(BEFORE_DIR, AFTER_DIR)
        if len(dircmp.left_list) != len(dircmp.common):
            raise RuntimeError("Check amount of search results before and after changing " + CONTENTBODY_MAXSIZE)

        for f in os.listdir(BEFORE_DIR):
            before_content = load_search_term_file(BEFORE_DIR + os.path.sep + f)
            before_relevance = before_content[1]
            after_content = load_search_term_file(AFTER_DIR + os.path.sep + f)
            after_relevance = after_content[1]
            if len(before_relevance) > 1 and len(after_relevance) > 1:
                ba_data = SearchTermDataAnalyzer(before_relevance, after_relevance).analyze()
                ba_data[0][BEFORE].append(float(before_content[0]))
                ba_data[0][AFTER].append(float(after_content[0]))
                self.__chart_data[f] = ba_data

    def save_chart_data(self):
        self.save_csv_file(before=True)
        self.save_csv_file(before=False)

    def save_csv_file(self, before=True):
        search_terms = list(self.__chart_data.keys())
        values = list(self.__chart_data.values())
        relevances = [v[0][BEFORE if before else AFTER][0] for v in values]
        durations = [v[0][BEFORE if before else AFTER][1] for v in values]
        with open(OUTPUT + os.path.sep + AFTER + '_' + CHART_DATA_FILE_CSV, 'w+') as f:
            writer = csv.writer(f)
            writer.writerows(zip(search_terms, relevances, durations))


class SearchTermDataAnalyzer:
    def __init__(self, before_data, after_data):
        self.__before_data = before_data
        self.__after_data = after_data

    def analyze(self):
        intersect = [d for d in self.__before_data if d in self.__after_data]
        rb = []
        ra = []
        sb = []
        sa = []
        for i in intersect:
            rb.append(self.__before_data[i][0])
            ra.append(self.__before_data[i][0])
            sb.append(self.__before_data[i][1])
            sa.append(self.__before_data[i][1])
        dcgb = dcg_score(np.asarray([rb]), np.asarray([sb]))
        dcga = dcg_score(np.asarray([rb]), np.asarray([sa]))
        search_term_data = [{BEFORE: [dcgb], AFTER: [dcga]}]
        return search_term_data


data_chart_builder = SearchDataChartBuilder()
data_chart_builder.calc_chart_data()
data_chart_builder.save_chart_data()
