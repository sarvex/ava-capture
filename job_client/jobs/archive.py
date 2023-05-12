#
# Copyright (c) 2017 Electronic Arts Inc. All Rights Reserved 
#

from __future__ import print_function
from __future__ import absolute_import

from builtins import object
import json
import shutil
import os
import re
import time
import logging
import threading
from sys import platform

from .base import BaseJob

class DeleteFiles(BaseJob):
    def __call__(self, parameters, pipe, log):

        params = json.loads(parameters)

        if 'files' in params:
            for f in params['files']:

                if os.path.exists(f):

                    pipe.send(f'Delete {f}')

                    # ED: Should this job fail if we cannot delete the files?
                    try:
                        os.remove(f)
                    except:
                        pass

    class Meta(object):
        description = 'Delete local of remote files'

class ExportTake(BaseJob):
    def __call__(self, parameters, pipe, log):

        params = json.loads(parameters)

        if 'root_export_path' not in params:
            raise Exception('Error in parameters, "root_export_path" not found')
        if 'nodes' not in params:
            raise Exception('Error in parameters, "nodes" not found')

        child_to_launch = []

        # Launch one child job for each node that needs to copy files
        for node_name in params['nodes']:
            file_list = params['nodes'][node_name]            

            child_params = {'file_list':file_list, 'root_export_path':params['root_export_path'], 'delete_source_files':True}

            child_launch_info = {
                'job_class': 'jobs.archive.CopyFiles',
                'params': json.dumps(child_params),
                'node_name': node_name,
                'req_gpu': False,
            }
            child_to_launch.append(child_launch_info)

        self.yieldToChildren(child_to_launch)

    class Meta(object):
        description = 'This job is used to copy files from a local folder to a network storage'

def safeCopyFile(src, dest, block_size=64*1024*1024, callback=None):  

    if os.path.exists(dest):
        os.remove(dest)

    with open(src, 'rb') as fin:
        with open(dest, 'wb') as fout:
            arr = fin.read(block_size)
            while arr != "":
                fout.write(arr)
                if callback:
                    callback(len(arr))
                arr = fin.read(block_size)

def nice_time(s):
    hours = s // 3600
    minutes = (s-3600*hours) // 60
    if hours>0:
        return '%d hours %d minutes' % (hours,minutes)
    seconds = int(s-3600*hours-60*minutes)
    return (
        '%d minutes %d seconds' % (minutes, seconds)
        if minutes > 0
        else '%d seconds' % seconds
    )

def nice_size(s):
    if s<1024:
        return "%d Bytes" % s
    s = s // 1024
    if s<1024:
        return "%d kB" % s
    s = s // 1024
    if s<1024:
        return "%d MB" % s
    s = s // 1024
    if s<1024:
        return "%d GB" % s
    s = s // 1024
    return "%d TB" % s

class ProgressPercentage(object):
        def __init__(self, src, pipe):
            self._filenames = src if type(src) is list else [src]
            self._size = sum(self.safe_get_size(f) for f in self._filenames)
            self._seen_so_far = 0
            self._lock = threading.Lock()
            self._start_time = time.time()
            self._file_index = 0
            self._pipe = pipe
        def safe_get_size(self, filename):
            size = 0
            try:
                if os.path.exists(filename):
                    size = os.path.getsize(filename)
            except:
                pass
            return size
        def next_file(self):
            self._file_index = self._file_index + 1
        def __call__(self, bytes_amount):
            with self._lock:
                self._seen_so_far += bytes_amount

                percent = 100.0 * self._seen_so_far / self._size if self._size > 0 else 0

                # Update stats
                elapsed = time.time() - self._start_time
                if elapsed > 0.0:
                    copy_speed = self._seen_so_far/elapsed

                # Compute estimated ETA
                eta = ''
                if copy_speed>0 and self._seen_so_far>0 and self._seen_so_far < self._size:
                    eta = f'{nice_time(max(self._size - self._seen_so_far, 0) / copy_speed)} remaining'

                self._pipe.send('Copying [%d%%] File %d of %d (%s/s) %s' % (int(percent), self._file_index+1,len(self._filenames),nice_size(int(copy_speed)), eta))

class CopyFiles(BaseJob):
    def __call__(self, parameters, pipe, log):

        params = json.loads(parameters)

        delete_src_files = 'delete_source_files' in params and params['delete_source_files']

        if 'file_list' in params:

            progress = ProgressPercentage([src for src,dest in params['file_list']], pipe)

            for i,t in enumerate(params['file_list']):

                src,dest = t

                # destination folder
                try:
                    os.makedirs(dest)
                except:
                    pass
                if not os.path.exists(dest):
                    raise Exception(f'Cannot create folder {dest}')

                dest_file = os.path.join(dest,os.path.split(src)[1])
                log.info(f'Copy {src} to {dest_file}')

                # Check if file already exists and should be skipped
                skip_file = False
                if os.path.exists(dest_file) and not os.path.exists(src):
                    log.info(f'Skip existing file: {dest_file}')
                    skip_file = True

                if not skip_file:
                    if not os.path.exists(src):
                        raise Exception(f'Source file does not exist: {src}')

                    file_size = os.path.getsize(src)

                    safeCopyFile(src, dest_file, callback=progress)

                    if not os.path.exists(dest_file):
                        raise Exception(f'Destination file does not exist: {dest_file}')
                    if os.path.getsize(dest_file) != file_size:
                        raise Exception(f'File size mismatch: {dest_file}')

                progress.next_file()

            # Everything copied, delete source files
            if delete_src_files:
                for src,dest in params['file_list']:
                    if os.path.exists(src):
                        log.debug(f'Deleting {src}')
                        try:
                            os.remove(src)
                        except:
                            log.error(f'Could not delete {src}')

        log.info('Done')

    class Meta(object):
        description = 'This job is used to copy files from a local folder to a network storage'

if __name__ == "__main__":

    # Test SafeCopyFile

    print('Test SafeCopyFile')

    src = r'C:\ava_capture\20170508_094614\26681150_000.avi'
    dest = r'C:\ava_capture\20170508_094614\26681150_000b.avi'

    safeCopyFile(src, dest, 8*1024*1024)
    