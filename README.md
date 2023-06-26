
# Alert Simulation App

This is a test app using FastAPI on the backend and React on the frontend.
The goal is to simulate a simple alerting system where a user can submit
a set of settings that define an alert and then trigger the simulation.

There is some basic single-session enforcement going on but no true authentication.
When starting a session, if another session is already in play, you are
asked to enter the management key in order to join the current session.


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
`docker run --rm --name my-redis -it -p 127.0.0.1:6379:6379 redis:latest`

RabbitMQ:  
`docker run --rm --name my-rabbit -it -p 127.0.0.1:5672:15672 -p 127.0.0.1:5672:5672 rabbitmq:3-management`

Postgres:  
`docker run --rm --name my-postgres -it -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:latest`


Under construction is a docker-compose.yml file that can be used launch all of these.


## To Do

This app was quickly cobbled together and no doubt has some rough edges.

A list of todo's:

1)  ~~There are no guardrails on the settings submitted by the frontend.
Right now, it's pretty trivially easy to DoS the backend. This should be
an easy fix.~~
*(FIXED)*

2)  ~~Somewhat related to the above, there is no error handling on the frontend.~~
Form entry validation should ideally happen on both frontend and backend
with the frontend being smart enough to display user-friendly errors.
*(PARTIALLY FIXED: Still needs guardrails on the server side.)*

3)  ~~There is no session management going on so if you hit the backend from
multiple browser windows, you'll likely see some odd results. What would
multi-session support look like? Would that just make it easier to tip
over the backend? Do I want instead to enforce a single session? For that,
I may then need to refactor the frontend a bit to query the backend for
appState instead of maintaining it in the browser instance.~~
*(FIXED: Single session enforcement has been added.)*

4)  So far, this repo contains two backend implementations; one using a
multiprocessor pool via `concurrent.futures`, and one using a simple Celery
solution with Redis as a queue. I would like to finish at least three more;
a multi-threaded version, a completely asyncio'd version, and maybe one
using AWS SQS + AWS Lambda.

5)  ~~The 'reset' actions for both current implementations are not robust enough.
It mostly works but sometimes processes are still left dangling or the queue is
not completely purged. I should diagnose and fix this.~~
*(PARTIALLY FIXED: Fixed most cases but probably needs more attention.)*

6)  More unit tests :)
