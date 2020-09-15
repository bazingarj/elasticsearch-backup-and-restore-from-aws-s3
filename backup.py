import config, sys
import elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch(config.ES_HOST)

if len(sys.argv) > 1:
	index_name = sys.argv[1]
	REPO_NAME = index_name+'-repo'
	SNAPSHOT_NAME = index_name+'-snapshot'
else:
	print('Enter Index Name e.g. python3 backup-and-delete.py my-index');

if len(sys.argv) > 2:
	BASE_PATH = sys.argv[2]
else:
	BASE_PATH = config.DEF_BASE_PATH

if es.indices.exists(index=index_name):
	print('')
else:
	print('Index "'+index_name+'" not Found');
	exit()

#check Snapshot	Exists
try:
	old_snap = es.snapshot.get(repository=REPO_NAME, snapshot=SNAPSHOT_NAME)
	print('Snapshot Already Exist')
	exit()
except elasticsearch.exceptions.NotFoundError:
	print('')



# Creating or Updating Repo
repoBody = { "type": "s3", "settings": { "bucket": config.S3_BUCKET_NAME, "base_path": BASE_PATH+'/'+SNAPSHOT_NAME, "region": config.S3_BUCKET_REGION }}
if es.snapshot.create_repository(REPO_NAME, verify=False, body=repoBody):
	print('Repo Updated')
else:
	print('Failed to create Repo, Please ensure elasticsearch plugin "S3 endpoint" is installed or not. Or Maybe The Repo Already Exists');
	exit()

#check Snapshot Exists
try:
	old_snap = es.snapshot.get(repository=REPO_NAME, snapshot=SNAPSHOT_NAME)
	print('Snapshot Already Exist')
	exit()
except elasticsearch.exceptions.NotFoundError:
	print('')

#creating Snapshot
index_body = { "indices": index_name }
if es.snapshot.create(repository=REPO_NAME, snapshot=SNAPSHOT_NAME, body=index_body, wait_for_completion=True, request_timeout=600):
	print('Snapshot created')
	if config.DELETE_REPO_AFTER_SNAPSHOT:
		es.snapshot.delete_repository(repository=REPO_NAME)
else:
	print('Error in creating Snapshot')
	exit()

