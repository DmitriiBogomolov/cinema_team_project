from diagrams import Diagram, Edge
from diagrams.c4 import Container
from diagrams.generic.device import Mobile
from diagrams.onprem.client import Client
from diagrams.onprem.database import ClickHouse, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python
from diagrams.elastic.elasticsearch import Elasticsearch


with Diagram('Sprint-8-as-is-architecture', show=False):
    admin_client = Client('admin')
    client = Mobile('client')

    nginx = Nginx('nginx')

    admin = Container(
        name='Admin',
        technology='Django',
        description='Django admin dashboard.',
    )
    auth = Container(
        name='Auth',
        technology='Flask',
        description='Authentication microservice.',
    )
    filmworks = Container(
        name='Filmworks API',
        technology='FastAPI',
        description='Filmworks API microservice.',
    )
    ugc = Container(
        name='UGC',
        technology='FastAPI',
        description='User generated content microservice.',
    )

    admin_client >> Edge(color='darkgreen') << nginx
    client >> Edge() << nginx

    nginx >> Edge(color='darkgreen') << admin
    nginx >> Edge() << auth
    nginx >> Edge() << filmworks
    nginx >> Edge() << ugc

    elastic = Elasticsearch('Elasticsearch')
    admin >> PostgreSQL('PostgreSQL') >> Python('Filmworks etl') >> elastic

    auth >> PostgreSQL('PostgreSQL')
    auth >> Redis('Redis')

    filmworks >> elastic
    filmworks >> Redis('Redis')

    ugc >> Kafka('Kafka') >> Python('UGC etl') >> ClickHouse('ClickHouse')
