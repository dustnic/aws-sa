#!/usr/bin/env python3

from aws_cdk import core

from aws_sa.FrontEndStack import FrontendStack
from aws_sa.DatabaseStack import DatabaseStack
from aws_sa.BackEndStack import BackendStack
from aws_sa.NetworkStack import NetworkStack

AWS_REGION = "eu-west-1"

app = core.App()

env = core.Environment(
    region = AWS_REGION
)

nw_stack = NetworkStack(app, "aws-sa-network", env=env)
fe_stack = FrontendStack(app, "aws-sa-frontend", env=env, network_stack=nw_stack)
be_stack = BackendStack(app, "aws-sa-backend", env=env)
db_stack = DatabaseStack(app, "aws-sa-database", env=env)

# tag = core.Tag('key','value')


        
        # # core.Tag('stack',self.stack_id).add(table)
        # # core.Tag('app','aws-cdk-threetier').add(table)
        # table.node.apply(core.Tag('Cost','Test'))

app.synth()
