#snapshotalyzer-6000

Demo project for practicing AWS CLI

##About

This is a demo project by Venu to practice AWS

#Configuring
Shotty uses the configuration file created by AWS CLI

 'aws configure --profile shotty'

#Running

Run the following command

'pipenv run python shotty/shotty.py command subcommand <--project=PROJECT>'

*command* is instances , volumes and snapshots
*subcommand* is list , start ,stop ,snapshot
*project* is optional
