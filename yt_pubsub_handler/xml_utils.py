import xml.etree.ElementTree as ET
import datetime

class PSH_XML():
    def __init__(self, data):
        self.data = data
        self.parse_yt_xml(xml_body=data)

    def parse_yt_xml(self, xml_body: str): 
        root = ET.fromstring(xml_body)
        entry = root.find("{http://www.w3.org/2005/Atom}entry")
        video_id = entry.find("{http://www.w3.org/2005/Atom}yt:videoId")
        channel_id = entry.find("{http://www.w3.org/2005/Atom}yt:channelId")
        title = entry.find("{http://www.w3.org/2005/Atom}title")
        published = entry.find("{http://www.w3.org/2005/Atom}published")
        updated = entry.find("{http://www.w3.org/2005/Atom}updated")
        
        published_dt, updated_dt = self._parse_xml_dates(published_dt, updated_dt)
        # accessors
        self.video_id = video_id
        self.channel_id = channel_id
        self.title = title
        self.published = published_dt
        self.updated = updated_dt

    def _parse_xml_dates(self, published_ts: str, updated_ts: str) -> (datetime.datetime, datetime.datetime):
        pblsh_ts = datetime.datetime.strptime(published_ts, "%y-%m-%dt%h:%m:%s%z")
        updt = self._rm_seconds_from_ts(updated_ts)
        updt_dt = datetime.datetime.strptime(updt, "%y-%m-%dt%h:%m:%s%z")
        return pblsh_dt, updt_dt

    def _rm_seconds_from_ts(self, ts: str) -> str:
        splt = ts.split(".")
        date_time = splt[0]
        tz_info = splt[-1].split("+")[-1]
        return "+".join(date_time, tz_info)

