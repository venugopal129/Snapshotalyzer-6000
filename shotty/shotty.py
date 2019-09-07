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
@instances.command('stop')
@click.option('--project',default=None,help='Only instances for project')
def stop_instances(project):
    "Stop EC2 Instances"
    instances=filter_instances(project)
    for i in instances:
        print('Stopping {0}....'.format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--project',default=None,help='starting instances for project <project_name')
def start_instanes(project):
    "start EC2 instances"
    instances=filter_instances(project)
    for i in instances:
        print('Starting {0}...'.format(i.id))
        i.start()

    return
if __name__=='__main__':
    instances()
