release: bash prod_setup.sh
web: gunicorn "yt_pubsub_handler:create_app()" --log-level=info
