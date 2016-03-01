from google.appengine.ext import db
from google.appengine.tools import bulkloader


""" Lazy copy-paste of the class model here because import wasn't working """
class ScanRecord(db.Model):
    visitor_id = db.IntegerProperty(required=True)
    exhibit_name = db.StringProperty(required=True)
    scan_time = db.DateTimeProperty(auto_now_add=True)




class ScanRecordExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'ScanRecord',
                                     [('visitor_id', str, ""),
                                      ('exhibit_name', str, ""),
                                      ('scan_time', str, "")
                                     ])


exporters = [ScanRecordExporter]