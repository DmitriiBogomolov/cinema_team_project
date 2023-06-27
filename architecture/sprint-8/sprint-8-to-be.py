from diagrams import Diagram, Edge, Cluster
from diagrams.c4 import Container
from diagrams.generic.device import Mobile
from diagrams.onprem.client import Client
from diagrams.onprem.database import ClickHouse, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python
from diagrams.elastic.elasticsearch import Elasticsearch


with Diagram('Sprint-8-to-be-architecture', show=False, direction='TB'):
    admin_client = Client('admin')
    client = Mobile('client')

    nginx = Nginx('nginx')

    with Cluster('Admin service'):
        admin_app = Container(
            name='Admin app',
            technology='Django',
            description='Django admin dashboard.',
        )
        admin_nginx = Nginx('Nginx')
        admin_nginx >> Edge() << admin_app
        admin_postgres = PostgreSQL('PostgreSQL')
        admin_app >> admin_postgres

    with Cluster('Auth service'):
        auth_app = Container(
            name='Auth app',
            technology='Flask',
            description='Authentication microservice.',
        )
        auth_nginx = Nginx('Nginx')
        auth_nginx >> Edge() << auth_app
        auth_postgres = PostgreSQL('PostgreSQL')
        auth_app >> auth_postgres
        auth_redis = Redis('Redis')
        auth_app >> auth_redis

    with Cluster('Filmworks service'):
        filmworks_app = Container(
            name='Filmworks API app',
            technology='FastAPI',
            description='Filmworks API microservice.',
        )
        filmworks_nginx = Nginx('Nginx')
        filmworks_nginx >> Edge() << filmworks_app
        filmworks_elastic = Elasticsearch('Elasticsearch')
        filmworks_app >> filmworks_elastic
        filmworks_redis = Redis('Redis')
        filmworks_app >> filmworks_redis
        filmworks_etl = Python('Filmworks etl')

    with Cluster('UGC service'):
        ugc_app = Container(
            name='UGC app',
            technology='FastAPI',
            description='User generated content microservice.',
        )
        ugc_nginx = Nginx('Nginx')
        ugc_nginx >> Edge() << ugc_app
        ugc_app >> Kafka('Kafka') >> Python('UGC etl') >> ClickHouse('ClickHouse')

    admin_client >> Edge(color='darkgreen') << nginx
    client >> Edge() << nginx

    nginx >> Edge(color='darkgreen') << admin_nginx
    nginx >> Edge() << auth_nginx
    nginx >> Edge() << filmworks_nginx
    nginx >> Edge() << ugc_nginx

    admin_postgres >> filmworks_etl >> filmworks_elastic
