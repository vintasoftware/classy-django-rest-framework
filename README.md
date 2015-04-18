# Classy Django REST Framework. (http://cdrf.co)

## Dependencies
* Python 2.7
* s3cmd (For deploy)

## Building

`pip install -r requirements.txt`

`fab build`

The first build will take a while.

To run locally:

`fab runserver`

## Deployment

create a .env file with the content:

```
BUCKET_NAME=''
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
```

and deploy via

`fab deploy`
