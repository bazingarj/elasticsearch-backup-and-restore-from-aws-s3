# elasticsearch-backup-and-restore-from-aws-s3
NOTE: Note role on ec2 with s3 access, or aws credentials setup beforehand.

STEP 1: install requirements from requirements.txt

``` sudo pip3 install -r requirements.txt ```

STEP 2: Define ES_HOST, S3_BUCKET_NAME, S3_BUCKET_REGION in config.py

ES_HOST = ['127.0.0.1:9200']

S3_BUCKET_NAME = ''

S3_BUCKET_REGION = ''

DELETE_REPO_AFTER_SNAPSHOT = False 

Note: set True to delete repo from elasticsearch after backup and restore operations, Also it can be used to create multiple backup of same index in separate folders

STEP 3 : Make Backup

``` python3 backup.py posts ```
OR 
``` python3 backup.py posts 'staging/year/month/' ```


STEP 4 : Restore Backup

``` python3 restore.py posts ```
OR 
``` python3 restore.py posts 'staging/year/month/' ```

Note: DELETE_REPO_AFTER_SNAPSHOT allows to keep same name backup in different folder
