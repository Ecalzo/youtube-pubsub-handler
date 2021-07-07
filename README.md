# What is this doing?
Youtube uses pubsubhub to send push notifications for new video uploads. This app subscribes when a user requests a channel ID to be linked to a subreddit. This handshake occurs when the app acknowledges the GET request from pubsubhub by serving its challenge in the http response (seen as `request.args["hub.challenge"]`). Now we should receive POST requests containing XML data about the new uploads for the YT channel the app is subscribed to. This app then regularly keep leases from pubsubhub "fresh" by renewing leases in its database that may expire in the near future.

# Endpoints
* `/pubsubhub/hook` the hook to use with [pubsubhub](https://pubsubhubbub.appspot.com/subscribe)
* `/subscriptions/new` endpoint for creating a new subscription for a channel + subreddit

# Deployment
1. `zappa deploy production` this will also create the bucket specified in the `s3_bucket` section of `zappa_settings.json`
2. Ensure that an `env.json` is in the bucket project
    * ex: if `"remote_env": "s3://zappa-yt-pubsub-handler-production/env.json"` then the `env.json` should be place in the appropriate bucket after deploy
3. Set up db: `zappa invoke production 'yt_pubsub_handler.db_utils.init_db'`

# env.json
```json
{
    "DATABASE_URL": "postgresql+psycopg2://user:pw@host/production",
    "SECRET_KEY": "dev", // see Flask docs for how to generate
    "client_id": "", // reddit client id for account that makes posts
    "client_secret": "", // reddit client_secret
    "reddit_password": "", // reddit pw
    "reddit_username": "", // reddit user
    "URL_ROOT": "https://root_of_your_site/" // for working outside flask request context
}
```

# Migrations
[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is used for migrations.

## Running migrations for the production application:
* Start a local flask session with `./local_dev.sh`
* Edit `yt_pubsub_handler/models.py` with your intended changes
* In a seperate terminal, make sure env variable is set: `export FLASK_APP=yt_pubsub_handler` 
* Run `flask db migrate` to automatically create a revision in the `migrations/versions` folder
    * **Review this thoroughly** and make any changes, alembic auto-generates these and they may sometimes contain flaws
* Commit your changes and submit PR. Once merged to master `zappa update production` will push the revision to the prod environment 
* to execute the migration in production: `zappa invoke production 'run.run_alembic_upgrade'`
    * for downgrade simply use `run_alembic_downgrade` instead
