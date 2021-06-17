from . import xml_utils
import datetime

test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
  <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
  <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCtEorrVfo4GQsN82HsrnKyk"/>
  <title>YouTube video feed</title>
  <updated>2018-12-12T06:02:55.950497732+00:00</updated>
  <entry>
    <id>yt:video:_em_FFNUcvs</id>
    <yt:videoId>_em_FFNUcvs</yt:videoId>
    <yt:channelId>UCtEorrVfo4GQsN82HsrnKyk</yt:channelId>
    <title>December 12, 20</title>
    <link rel="alternate" href="https://www.youtube.com/watch?v=_em_FFNUcvs"/>
    <author>
      <name>Ak Ram</name>
      <uri>https://www.youtube.com/channel/UCtEorrVfo4GQsN82HsrnKyk</uri>
    </author>
    <published>2018-12-12T05:57:07+00:00</published>
    <updated>2018-12-12T06:02:55.950497732+00:00</updated>
  </entry>
</feed>"""


def test_xml_utils():
    xml = xml_utils.PSH_XML(test_xml)

    assert xml.video_id == "_em_FFNUcvs"
    assert xml.channel_id == "UCtEorrVfo4GQsN82HsrnKyk".upper()
    assert xml.title == "December 12, 20"
    assert xml.url == "https://www.youtube.com/watch?v=_em_FFNUcvs"
    assert xml.published == datetime.datetime(2018, 12, 12, 5, 57, 7, tzinfo=datetime.timezone.utc)
    assert xml.updated == datetime.datetime(2018, 12, 12, 6, 2, 55, tzinfo=datetime.timezone.utc)
