import xml.etree.ElementTree as ET
import datetime

class PSH_XML():
    def __init__(self, data):
        self.data = data
        parse_yt_xml(xml_body=data)

    def parse_yt_xml(self, xml_body: str): 
        root = ET.fromstring(xml_body)
        entry = root.find("{http://www.w3.org/2005/Atom}entry")
        video_id = entry.find("{http://www.w3.org/2005/Atom}yt:videoId")
        channel_id = entry.find("{http://www.w3.org/2005/Atom}yt:channelId")
        title = entry.find("{http://www.w3.org/2005/Atom}title")
        published = entry.find("{http://www.w3.org/2005/Atom}published")
        updated = entry.find("{http://www.w3.org/2005/Atom}updated")
        
        published_dt, updated_dt = parse_xml_dates(published_dt, updated_dt)
        # accessors
        self.video_id = video_id
        self.channel_id = channel_id
        self.title = title
        self.published = published_dt
        self.updated = updated_dt

    def parse_xml_dates(published_ts, updated_ts):
        # TODO: parse timezone info for database cols
        # pop off any strange nanoseconds and timezone info
        # published and updated look differently...
        pblsh = published_ts.split("+")[0]
        updt = updated_ts.split(".")[0]
        pblsh_dt = datetime.datetime.strptime(pblsh, "%Y-%m-%dT%H:%M:%S")
        updt_dt = datetime.datetime.strptime(updt, "%Y-%m-%dT%H:%M:%S")
        return pblsh_dt, updt_dt
