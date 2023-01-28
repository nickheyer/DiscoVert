#!/bin/sh

PORT=7200

gunicorn --bind 0.0.0.0:$PORT DiscoVert.api:app
echo "Shutting down Gunicorn Server"