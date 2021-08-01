#!/bin/bash

docker build . -t api-deployment
heroku container:login
heroku container:push web --app ancient-journey-94670
heroku container:release web --app ancient-journey-94670
