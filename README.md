# What is this doing?
pubsubhub sends push notifications for new video uploads. We subscribe with one of the links above and acknowledge the GET request from pubsubhub by serving its challenge, seen as `request.args["hub.challenge"]` in `app.py`. Now we should receive POST requests containing XML data about the new uploads for the YT channel we subscribed to. Thats it for now, in the future we would like to integrate this into a reddit mod bot to post about the new uploads.

# Endpoints
* `/pubsubhub/hook` the hook to use with [pubsubhub](https://pubsubhubbub.appspot.com/subscribe)
* `/subscription/new` endpoint for creating a new subscription for a channel + subreddit

# Deployment
1. `zappa deploy production` this will also create the bucket specified in the `s3_bucket` section of `zappa_settings.json`
2. Ensure that an `env.json` is in the bucket project
    * ex: if `"remote_env": "s3://zappa-yt-pubsub-handler-production/env.json"` then the `env.json` should be place in the appropriate bucket after deploy

# env.json
```json
{
    "DATABASE_URL": "postgresql+psycopg2://user:pw@host/production",
    "SECRET_KEY": "dev", // see Flask docs for how to generate
    "client_id": "", // reddit client id for account that makes posts
    "client_secret": "", // reddit client_secret
    "reddit_password": "", // reddit pw
    "reddit_username": "" // reddit user
}
```