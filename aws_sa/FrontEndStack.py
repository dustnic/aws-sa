from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_certificatemanager as acm

INSTANCE_TYPE = "t3a.micro"
# INSTANCE_AMI = "ami-0bbc25e23a7640b9b"

class FrontendStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, network_stack: core.Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # self.env = env

        self.network_stack = network_stack

        self.logs_bucket = self.__create_logs_bucket__()
    
        self.alb_security_group, self.frontend_security_group = self.__create_security_groups__()

        self.asg = self.__create_asg__()
        
        self.alb = self.__create_application_load_balancer__()
    

    def __create_logs_bucket__(self):
        bucket = s3.Bucket(
            self,
            "frontend-alb-logs-bucket",
            access_control=s3.BucketAccessControl.PRIVATE
        )
        return bucket

    def __create_asg__(self):
        asg = autoscaling.AutoScalingGroup(
            self,
            "frontend-autoscaling-group",
            instance_type = ec2.InstanceType(INSTANCE_TYPE),
            machine_image = ec2.AmazonLinuxImage(),
            vpc = self.network_stack.vpc,
            vpc_subnets = ec2.SubnetSelection(one_per_az=True,subnet_type=ec2.SubnetType.PUBLIC),
            desired_capacity = 2
        )
        asg.add_security_group(self.frontend_security_group)
        return asg
    
    def __create_security_groups__(self):
        alb_security_group = ec2.SecurityGroup(
            self,
            "alb_frontend_security_group",
            security_group_name="alb_frontend_security_group",
            vpc = self.network_stack.vpc,
            allow_all_outbound=False
        )
        
        frontend_security_group = ec2.SecurityGroup(
            self,
            "ec2_frontend_security_group",
            vpc = self.network_stack.vpc,
            security_group_name="ec2_frontend_security_group",
            allow_all_outbound=False
        )
        
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80)
        )

        alb_security_group.add_egress_rule(
            frontend_security_group,
            ec2.Port.tcp(80)
        )

        frontend_security_group.add_ingress_rule(
            alb_security_group,
            ec2.Port.tcp(80)
        )

        return alb_security_group, frontend_security_group

    def __create_application_load_balancer__(self):
        alb = elb.ApplicationLoadBalancer(
            self,
            "frontend-alb",
            security_group = self.alb_security_group,
            vpc = self.network_stack.vpc,
            vpc_subnets = ec2.SubnetSelection(one_per_az=True,subnet_type=ec2.SubnetType.PUBLIC),
            internet_facing = True,
            load_balancer_name="acme-frontend-public-alb"
        )
        
        alb_listener_http = elb.ApplicationListener(
            self,
            "frontend-alb-http-listener",
            load_balancer=alb,
            port=80
        )
        
        alb.log_access_logs(self.logs_bucket)

        return alb

