docker pull nginx:latest

docker pull phpdockerio/php73-fpm

docker run --name  myphp-fpm -v /media/totem_disk/totem/kwong/ai_rom_demo/www:/www -d phpdockerio/php73-fpm

mkdir -p nginx/conf/conf.d

vi nginx/conf/conf.d/ai_rom_test_php.conf

cat nginx/conf/conf.d/ai_rom_test_php.conf

docker run --name ai_rom_php_test -p 8083:80 -d -v /media/totem_disk/totem/kwong/ai_rom_demo/www:/usr/share/nginx/html:ro -v /media/totem_disk/totem/kwong/ai_rom_demo/nginx/conf/conf.d:/etc/nginx/conf.d:ro --link myphp-fpm:php nginx

docker cp ../nginx/nginx.conf nginx:/etc/nginx/nginx.conf
