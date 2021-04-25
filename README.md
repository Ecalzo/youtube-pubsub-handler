# Readings/Debugging
* https://stackoverflow.com/questions/3007253/send-post-xml-file-using-curl-command-line
* https://stackoverflow.com/questions/49901197/flask-api-to-parse-xml-post-requests-returning-errors
* https://stackoverflow.com/questions/10999990/get-raw-post-body-in-python-flask-regardless-of-content-type-header
* https://blog.superfeedr.com/howto-pubsubhubbub/
* https://pubsubhubbub.appspot.com/subscribe
* https://developers.google.com/youtube/v3/guides/push_notifications

random SO links to save while I'm switching computers

# Test out the endpoint
```shell
$ python3 app.py
# open a separate terminal window and send some provided test data
$ curl -X POST -d @test.xml http://127.0.0.1:5000/receive
```

# What is this doing?
pubsubhub sends push notifications for new video uploads. We subscribe with one of the links above and acknowledge the GET request from pubsubhub by serving its challenge, seen as `request.args["hub.challenge"]` in `app.py`. Now we should receive POST requests containing XML data about the new uploads for the YT channel we subscribed to. Thats it for now, in the future we would like to integrate this into a reddit mod bot to post about the new uploads.

# Roadmap
* Users provide `channel_id` and `subreddit` and from there we can decide where we need to post when we receive a new video from a given channel ID
	1. receive new post request for a new video
	2. check if the video has already been posted - short circuit if it has
	3. else, check which subreddits are queried per channel ID
	4. `models.Subscriptions.query.filter_by(channel_id=channel_id)` then parse out all values in the subreddit column

TODO:
* !!!start blueprint for registering a new subreddit - this is prob the most important
* write tests for xml_utils
* start database tests 
