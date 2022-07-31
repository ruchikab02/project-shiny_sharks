#!/bin/bash
curl --request POST http://localhost:5000/api/timeline_post -d 'name=Ruchika&email=ruchika.bee@gmail.com&content=Just Added Database to my portfolio site!'
curl http://localhost:5000/api/timeline_post