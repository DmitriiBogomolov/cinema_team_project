from diagrams import Diagram, Cluster
from diagrams.c4 import Container
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.aws.engagement import Pinpoint


with Diagram('Sprint-8-UGC-decomposition', show=False, direction='TB'):
    nginx = Nginx('nginx')

    with Cluster('FastAPI app'):
        endpoint = Pinpoint('Endpoint')
        token_checker = Container(
            name='Tocken checker',
            technology='async_fastapi_jwt_auth',
            description='Checks token and roles.',
        )
        serializer = Container(
            name='Serializer',
            technology='pydantic',
            description='Validate and serialize data',
        )

        endpoint >> token_checker >> serializer

    nginx >> endpoint
    serializer >> Kafka('Kafka')
    serializer >> Redis('Redis')
