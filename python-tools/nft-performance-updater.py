import glob
import os
import shutil

from git import Git

jmeter_nft_prod = "c:\\Applications\\jmeter-nft-prod" + os.sep
nft_performance = "git@github.wdf.sap.corp:nft/nft2.0_performance.git"
nft_performance_dir = "c:\\src\\nft2.0_performance" + os.sep
ignore_patterns = ""
enwiki = "ENWIKI"
g = Git(nft_performance_dir)
g.checkout(nft_performance_dir, force=True)
# remove influx files
influxdata_file_list = glob.glob(jmeter_nft_prod + 'InfluxData2Send*', recursive=True)
for f in influxdata_file_list:
    try:
        os.remove(f)
    except OSError:
        print("Error while deleting influx files")

# copy ENWIKI to run folder
shutil.copytree(nft_performance_dir + enwiki, jmeter_nft_prod + enwiki,
                ignore=shutil.ignore_patterns('*service.properties', 'main.properties'), dirs_exist_ok=True)
