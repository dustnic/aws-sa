from aws_cdk import core
from aws_cdk import aws_ec2 as ec2

APP = "AWS-SA"
VPC_CIDR = "172.15.0.0/20"
VPC_ID = "acme_com_vpc"

class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc =  self.__create_vpc__()

    def __create_vpc__(self):
        subnet_configurations = [
            ec2.SubnetConfiguration(
                name='Public',
                subnet_type = ec2.SubnetType.PUBLIC,
                cidr_mask=24
            ),
            ec2.SubnetConfiguration(
                name='Private',
                subnet_type = ec2.SubnetType.ISOLATED,
                cidr_mask=24
            ),

        ]
        
        vpc = ec2.Vpc(
            self,
            VPC_ID,
            subnet_configuration=subnet_configurations,
            cidr=VPC_CIDR
        )

        return vpc