import os
import csv
import xml.etree.ElementTree as ET
import datetime

def parse_yt_xml(xml_body: str) -> (str, str):
    with open('log.xml', 'a') as xml_log:
        xml_log.write(xml_body)

    root = ET.fromstring(xml_body)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
    channel_id = entry.find("{http://www.youtube.com/xml/schemas/2015}channelId").text
    title = entry.find("{http://www.w3.org/2005/Atom}title") 
    link = entry.find("{http://www.w3.org/2005/Atom}link")
    published = entry.find("{http://www.w3.org/2005/Atom}published")
    updated = entry.find("{http://www.w3.org/2005/Atom}updated")
    is_new = is_new_upload_v2(video_id, channel_id)
    return title.text, link.attrib["href"], is_new


def is_new_upload_v2(video_id: str, channel_id: str):
    fname = f"/app/{channel_id}.csv"
    if not os.path.isfile(fname):
        open(fname, 'a').close()

    with open(fname, 'a') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if video_id in row:
                return False  # not a new upload

    with open(fname, "a") as csvfile:
        print(f"writing file {fname}")
        writer = csv.writer(csvfile)
        writer.writerow([video_id])
        return True


def is_new_upload(published_ts: str, updated_ts: str) -> bool:
    # pop off any strange nanoseconds and timezone info
    # published and updated look differently...
    pblsh = published_ts.split("+")[0]
    updt = updated_ts.split(".")[0]
    pblsh_dt = datetime.datetime.strptime(pblsh, "%Y-%m-%dT%H:%M:%S")
    updt_dt = datetime.datetime.strptime(updt, "%Y-%m-%dT%H:%M:%S")
    diff = (updt_dt - pblsh_dt)
    if hasattr(diff, "seconds"):
        return diff.seconds < (60 * 10) # 10 min
    else:
        return True


if __name__ == "__main__":
    with open("test.xml", "r") as xml_file:
        text = xml_file.read()
        title, link, is_new = parse_yt_xml(text)
        print(is_new)     
