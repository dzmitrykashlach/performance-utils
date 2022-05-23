import filecmp
import os

SCRIPTS_DIR = r'\stag\main\plan'
ENWIKI_DIR = os.getcwd() + os.path.sep + r'ENWIKI' + SCRIPTS_DIR
SCNWIKI_DIR = os.getcwd() + os.path.sep + r'SCNWIKI' + SCRIPTS_DIR

CONTENTBODY_MAXSIZE = r"contentbody.maxsize"


class NFTScriptsDiffBuilder:
    def __init__(self):
        self.__chart_data = {}

    def calc_diff(self):
        # Check that number of files and filenames are equal in both directories
        dircmp = filecmp.dircmp(ENWIKI_DIR, SCNWIKI_DIR)
        print(dircmp.right_only)
        print(dircmp.left_only)
        print(dircmp.diff_files)


data_chart_builder = NFTScriptsDiffBuilder()
data_chart_builder.calc_diff()
