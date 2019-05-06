import argparse

import googleapiclient.discovery

def create_cluster(dataproc, project, zone, region, cluster_name):
    print('Creating cluster...')
    zone_uri = \
        'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(
            project, zone)
    cluster_data = {
        'projectId': project,
        'clusterName': cluster_name,
        'config': {
            'gceClusterConfig': {
                'zoneUri': zone_uri
            },
            'masterConfig': {
                'numInstances': 1,
                'machineTypeUri': 'n1-standard-1'
            },
            'workerConfig': {
                'numInstances': 2,
                'machineTypeUri': 'n1-standard-1'
            }
        },
        #'initializationActions': [
          #{
          # 'executableFile': 'gs://dataproc-initialization-actions/jupyter/jupyter.sh'
          #},
        #],
    }
    result = dataproc.projects().regions().clusters().create(
        projectId=project,
        region=region,
        body=cluster_data).execute()
    return result
# [END create_cluster]

def wait_for_cluster_creation(dataproc, project_id, region, cluster_name):
    print('Waiting for cluster creation...')

    while True:
        result = dataproc.projects().regions().clusters().list(
            projectId=project_id,
            region=region).execute()
        cluster_list = result['clusters']
        cluster = [c
                   for c in cluster_list
                   if c['clusterName'] == cluster_name][0]
        if cluster['status']['state'] == 'ERROR':
            raise Exception(result['status']['details'])
        if cluster['status']['state'] == 'RUNNING':
            print("Cluster created.")
            break

def get_client():
    """Builds an http client authenticated with the service account
    credentials."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc

def get_region_from_zone(zone):
    try:
        region_as_list = zone.split('-')[:-1]
        return '-'.join(region_as_list)
    except (AttributeError, IndexError, ValueError):
        raise ValueError('Invalid zone provided, please check your input.')

def main(project_id, zone, cluster_name, create_new_cluster = True):
    dataproc = get_client()
    region = get_region_from_zone(zone)
    create_cluster(dataproc, project_id, zone, region, cluster_name)
    wait_for_cluster_creation(dataproc, project_id, region, cluster_name)
    print 'Cluster has been created with jupyter'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True),
    parser.add_argument(
        '--zone', help='Zone to create clusters in/connect to', required=True)
    parser.add_argument(
        '--cluster_name',
        help='Name of the cluster to create/connect to', required=True)
    parser.add_argument(
        '--create_new_cluster',
        action='store_true', help='States if the cluster should be created')

    args = parser.parse_args()
    main(args.project_id, args.zone, args.cluster_name,args.create_new_cluster)
