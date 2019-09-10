import boto3
import click
session=boto3.Session(profile_name='shotty')
ec2=session.resource('ec2')
def filter_instances(project):
    instance=[]

    if project:
        filters=[{'Name':'tag:Project','Values':[project]}]
        instances=ec2.instances.filter(Filters=filters)
    else:
        instances=ec2.instances.all()
    return instances
@click.group()
def cli():
    """Shooty manages snapshots"""
@cli.group('snapshots')
def snapshots():
    """Commands for snapshotps"""
@snapshots.command('list')
@click.option('--project',default=None,help="only snapshots of volmes for poject(tag Project:<name>)")
def list_snapshots(project):
    """List snapshots of volumes for a project"""
    instances=filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))
    return

@cli.group('volumes')
def volumes():
    """commands for volumes"""
@volumes.command('list')
@click.option('--project',default=None,help="only volumes for poject(tag Project:<name>)")
def list_volumes(project):
    """List volumes for a project"""
    instances=filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size)+" GB",
                v.encrypted and "Encrypted" or "Not Encrypted")))

    return


@cli.group('instances')
def instances():
    """Commands for Intsances"""
@instances.command('list')
@click.option('--project',default=None,help="only instance for poject(tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances=filter_instances(project)
    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        print(','.join((i.id,
            i.instance_type,
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no_project>'))))


    return

@instances.command('snapshot')
@click.option('--project',default=None,help='Only instances for project')
def create_snapshot(project):

    """Creates snapshots for a project """
    instances=filter_instances(project)
    for i in instances:
        i.stop()
        print('Waiting for instance {0} to stop...'.format(i.id))
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snapshot for volume {0}...".format(v.id))
            v.create_snapshot(Description='Created by snapshotalyzer code')
        i.start()
        print('Waiting for instance {0} to start...'.format(i.id))
        i.wait_until_running()
    print ('snapshot is complete')
    return
@instances.command('stop')
@click.option('--project',default=None,help='Only instances for project')
def stop_instances(project):
    "Stop EC2 Instances"
    instances=filter_instances(project)
    for i in instances:
        print('Stopping {0}....'.format(i.id))
        try:
            i.stop()
        except boto3.exceptions.botocore.exceptions.ClientError as e:
            print('Cannot stop instance {0}..'.format(i.id)+str(e))
            continue
    return

@instances.command('start')
@click.option('--project',default=None,help='starting instances for project <project_name')
def start_instanes(project):
    "start EC2 instances"
    instances=filter_instances(project)
    for i in instances:
        print('Starting {0}...'.format(i.id))
        try:
            i.start()
        except boto3.exceptions.botocore.exceptions.ClientError as e:
            print('Cannot start instance {0}..'.format(i.id)+str(e))
            continue

    return
if __name__=='__main__':
    cli()
