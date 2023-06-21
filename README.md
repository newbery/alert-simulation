
# Alert Simulation App

See http://digitalmarbles.com/alert-simulation.html for details.


## Getting Started

See "SETUP_BACKEND.md" for instructions on how to set up the python environment
and to run the main FastAPI service.

See "SETUP_FRONTEND.md" for instructions on how to set up the javascript environment
to run the React frontend in "development mode" or to build a static version of the
frontend to be served directly via FastAPI. 


## Services

Depending on which FastAPI/celery backend implementation is enabled,
some external services may be required.

Redis:  
`docker run --rm --name my-redis -it -p 6379:6379 redis:latest`

RabbitMQ:  
`docker run --rm --name my-rabbit -it -p 15672:15672 -p 5672:5672 rabbitmq:3-management`

Postgres:  
`docker run --rm --name my-postgres -it -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:latest`


Under construction is a docker-compose.yml file that can be used launch all of these.

