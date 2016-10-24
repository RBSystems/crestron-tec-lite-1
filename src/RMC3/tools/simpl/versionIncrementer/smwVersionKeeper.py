#!/usr/bin/env python
import sys
import re
import time
import logging
import fileinput
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class VersionUpdater(PatternMatchingEventHandler):
    patterns = ["*.smw"]

    def increment(self,event):
        try:
            # In SMW increment JpNo=4.6.11
            f = open(event.src_path,'r')
            filedata = f.read()
            f.close()
            versionNumber = re.findall ( 'JpNo=(.*?)\n', filedata, re.DOTALL)
            pitLine = re.findall ( 'PIT=TEC_Lite_(.*?)\n', filedata, re.DOTALL)


            a = versionNumber[0].split('.')
            lastNum = a[-1]
            try:
                incremented = int(lastNum) + 1
            except ValueError as ex:
                logging.error(ex,ex.args)

            newVersion = None

            for item in a[:-1]:
                newVersion = "%s.%d" % (newVersion,incremented)
            newVersion = "%s.%s" % (newVersion,a[-1])

            underscored = newVersion.replace('.','_')

            newdata = filedata.replace("JpNo=%s" % versionNumber,"JpNo=%s" % newVersion)

            # In SMW increment PIT=TEC_Lite_4_6_11
            newestData = newdata.replace("PIT=TEC_Lite_%s" % pitLine, "PIT=TEC_Lite_%s" % underscored)
            f = open(event.src_path,'w')
            f.write(newestData)
            f.close()

        except Exception as ex:
            logging.error(ex,ex.args)


    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        self.increment(event)

    def on_modified(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(VersionUpdater(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
