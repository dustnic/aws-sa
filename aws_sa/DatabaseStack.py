from aws_cdk import core
# from aws_cdk import cdk
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ec2 as ec2

APP = "AWS-SA"
TIER = "database"
TABLE_ID = "acme_com_table"

class DatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # The code that defines your stack goes here
        table = self.__create_dynamodb_table__()    
        self.__apply_tags__()

    def __apply_tags__(self):
        core.Tag.add(self,'stack-id',self.stack_id)
        core.Tag.add(self,'app',APP)
        core.Tag.add(self,'tier',TIER)
        
    def __create_dynamodb_table__(self):
        ## DynamoDB table
        table = dynamodb.Table(
                self,
                TABLE_ID,
                partition_key={'name': 'path', 'type': dynamodb.AttributeType.STRING}
        )

        return table 

    def __create_dynamodb_endpoints__(self):
        pass

    def __create_dynamodb_endpoints_security_group__(self):
        pass
        ## DynamoDB VPC GW Endpoint SG