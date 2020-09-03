docker build . -t simple_det_image
docker run --name simple_det_server -d -p 8082:8082 simple_det_image
#在浏览器访问本机ip地址:8082/stage1_upload.html就可以访问页面，以本机访问为例:
#http://127.0.0.1:8082/stage1_upload.html
