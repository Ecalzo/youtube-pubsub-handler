from . import subscriptions_utils

def test_validate_yt_channel(app):
    channel_id = "UCYO_jab_esuFRV4b17AJtAw"
    channel_id_fls = "XYUCXZC_DSA_sad"
    channel_id_fls_2 = "UCYO_jc"
    with app.app_context():
        assert subscriptions_utils.validate_yt_channel(channel_id) == True
        assert subscriptions_utils.validate_yt_channel(channel_id_fls) == False
        assert subscriptions_utils.validate_yt_channel(channel_id_fls_2) == False

def test_validate_subreddit():
    assert subscriptions_utils.validate_subreddit("pics") == True

