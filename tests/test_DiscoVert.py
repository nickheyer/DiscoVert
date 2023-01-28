import os
import pytest
import shutil
import sys
import glob
sys.path.append("../DiscoVert")
import DiscoVert.DiscoVert as dv
import ffmpeg
from pprint import pprint

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
    )

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'cache')
WAITING_DIR = os.path.join(CACHE_DIR, 'waiting')
INCOMPLETE_DIR = os.path.join(CACHE_DIR, 'incomplete')
COMPLETE_DIR = os.path.join(CACHE_DIR, 'complete')

def cleanup_dir():
    files = glob.glob(CACHE_DIR + '/**/*.*', recursive=True)
    for file in files:
        os.remove(file)

def setup_test_data():
    cleanup_dir()
    files = [os.path.join(TEST_DATA_DIR, name) for name in os.listdir(TEST_DATA_DIR) if os.path.isfile(os.path.join(TEST_DATA_DIR, name))]
    for file in files:
        dest = os.path.join(WAITING_DIR, os.path.basename(file))
        shutil.copyfile(file, dest)

def move_file(src, dest):
    move = shutil.move(src, dest)
    print(move)
    return move

def test_sanity():
    print('testing sanity')
    assert 1 == 1

def test_convert():

    setup_test_data()

    
    for clip in os.listdir(WAITING_DIR):
        in_file = os.path.join(WAITING_DIR, clip)

        file_type = in_file.split('.')[-1]

        out_file = os.path.join(INCOMPLETE_DIR, f'tmp.{file_type}')
        
        metadata = { 'artist': 'discovert' }
        dv.change_metadata(in_file, out_file, metadata)
        
        
        out_file = move_file(out_file, os.path.join(COMPLETE_DIR, clip))
        probe = ffmpeg.probe(out_file)

        assert probe['format']['tags'].get('artist', None) == 'discovert'
