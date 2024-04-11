import os

import numpy as np

BODY_CONTENT = os.getcwd() + os.path.sep + r'bodycontent-prevver-null.csv'
body_content_length = []

with open(BODY_CONTENT) as f:
    body_content_length = [int(str.split(';')[0].replace('"', '')) for str in f]
    print('90% line = ' + str(np.percentile(body_content_length, 90)))
    print('95% line = ' + str(np.percentile(body_content_length, 95)))
    print('99% line = ' + str(np.percentile(body_content_length, 99)))
    print('100% line = ' + str(np.percentile(body_content_length, 100)))
