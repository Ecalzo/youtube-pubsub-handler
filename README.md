# Readings/Debugging
* https://stackoverflow.com/questions/3007253/send-post-xml-file-using-curl-command-line
* https://stackoverflow.com/questions/49901197/flask-api-to-parse-xml-post-requests-returning-errors
* https://stackoverflow.com/questions/10999990/get-raw-post-body-in-python-flask-regardless-of-content-type-header
* https://blog.superfeedr.com/howto-pubsubhubbub/

random SO links to save while I'm switching computers

# Test out the endpoint
```shell
$ python3 app.py
# open a separate terminal window and send some provided test data
$ curl -X POST -d @test.xml http://127.0.0.1:5000/receive
```
