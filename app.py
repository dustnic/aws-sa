#!/usr/bin/env python3

from aws_cdk import core

from aws_sa.aws_sa_stack import AwsSaStack


app = core.App()
AwsSaStack(app, "aws-sa")

app.synth()
