cd ../simple_det_image/
docker build . -t simple_det_image
docker run --name simple_det_server -d -p 8000:8000 simple_det_image
