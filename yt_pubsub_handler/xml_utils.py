import xml.etree.ElementTree as ET
import datetime


class PSH_XML():
    def __init__(self, data):
        self.data = data
        self.parse_yt_xml(xml_body=data)

    def parse_yt_xml(self, xml_body: str):
        root = ET.fromstring(xml_body)
        entry = root.find("{http://www.w3.org/2005/Atom}entry")
        video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
        channel_id = entry.find("{http://www.youtube.com/xml/schemas/2015}channelId").text
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        url = entry.find("{http://www.w3.org/2005/Atom}link").attrib["href"]
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        updated = entry.find("{http://www.w3.org/2005/Atom}updated").text

        published_dt, updated_dt = self._parse_xml_dates(published, updated)
        # accessors
        self.video_id = video_id
        self.channel_id = channel_id
        self.title = title
        self.url = url
        self.published = published_dt
        self.updated = updated_dt

    def _parse_xml_dates(self, published_ts: str, updated_ts: str) -> (datetime.datetime, datetime.datetime):
        pblsh_ts = datetime.datetime.strptime(published_ts, "%Y-%m-%dT%H:%M:%S%z")
        updt = self._rm_seconds_from_ts(updated_ts)
        updt_ts = datetime.datetime.strptime(updt, "%Y-%m-%dT%H:%M:%S%z")
        return pblsh_ts, updt_ts

    def _rm_seconds_from_ts(self, ts: str) -> str:
        splt = ts.split(".")
        date_time = splt[0]
        tz_info = splt[-1].split("+")[-1]
        return "+".join([date_time, tz_info])
