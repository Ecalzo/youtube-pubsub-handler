from utils.xml_parser import is_new_upload


def test_is_new_upload():
    published_ts = "2021-04-11T15:36:03+00:00"
    updated_ts = "2021-04-11T15:36:20.315657173+00:00"
    later_updated_ts = "2021-04-11T15:46:20.315657173+00:00" 

    assert is_new_upload(published_ts, updated_ts) == True
    assert is_new_upload(published_ts, later_updated_ts) == False 


