import os
import re


GS_PATTERN = r'gs://(.[^/]*)/(.*)'


def get_bucket_name(gs_path):
    bucket_and_dir_path = os.path.dirname(gs_path)
    match = re.match(GS_PATTERN, bucket_and_dir_path)
    if match:
        return match.group(1)
