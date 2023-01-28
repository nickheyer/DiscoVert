import ffmpeg
import json
import os

def change_metadata(in_file: str, out_file: str, metadata: dict):
    metadata_str = ','.join(f'{k}={v}' for k, v in metadata.items())
    (
        ffmpeg
        .input(in_file)
        .output(out_file, metadata=metadata_str)
        .run(overwrite_output=True)
    )
    os.remove(in_file)