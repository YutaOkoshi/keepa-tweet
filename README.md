# keepa-twitter



# for developer

## ! Prerequisite !

- Register with twitter developer to create an app and get a key and token.
  - https://developer.twitter.com/en/portal/dashboard
- Create a GCP service account with editing permissions and download secure.json
  - https://console.cloud.google.com/iam-admin/serviceaccounts
- spread sheet should be created as follows
  - ![スクリーンショット 2021-05-20 3 15 30](https://user-images.githubusercontent.com/37532269/118864006-7fd6bd80-b91a-11eb-8494-1c99ee6da168.png)
  - ![スクリーンショット 2021-05-20 3 16 45](https://user-images.githubusercontent.com/37532269/118864013-836a4480-b91a-11eb-9807-f5a27d2cd3ec.png)
 

## initial setup
```
# 1. make .env
$ cp .env,example .env

# 2. edit .env
$ vi .env
AFF_TAG=${Amazon Affiliate Tag}
API_KEY=${Twitter App API Key}
API_SECRET_KEY=${Twitter App API Secret Key}
ACCESS_TOKEN=${Twitter App API Access Token}
ACCESS_SECRET_TOKEN=${Twitter App API Secret Token}

# 3. Put the downloaded secure.json in the same location as main.py

# 4. install python 3.9
$ pyenv local 3.9.2

# 5. create & active virtual env
$ python -m venv venv
$ source venv/bin/activate

# 6. pip install
(venv)$ pip install -r requirements.txt
```


## gcloud deploy from local

```
$ gcloud -v
Google Cloud SDK 340.0.0

$ gcloud functions deploy keepa-twitter-function --trigger-topic "keepa-twitter-topic" --runtime python39 --region=asia-northeast1
```


## local run

- !Local development is not expected.!

```
# port listing to start function
(venv)$ functions_framework --target=main --debug

# another terminal
## http
(venv)$ curl localhost:8080 \
  -X POST \
  -H "Content-Type: application/json" \
  -H "ce-id: 123451234512345" \
  -H "ce-specversion: 1.0" \
  -H "ce-time: 2020-01-02T12:34:56.789Z" \
  -H "ce-type: google.cloud.pubsub.topic.v1.messagePublished" \
  -H "ce-source: //pubsub.googleapis.com/projects/MY-PROJECT/topics/MY-TOPIC" \
  -d '{
        "message": {
          "data": "d29ybGQ=",
          "attributes": {
             "attr1":"attr1-value"
          }
        },
        "subscription": "projects/MY-PROJECT/subscriptions/MY-SUB"
      }'
```
