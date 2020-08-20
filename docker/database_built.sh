docker pull mysql:8
docker run --name testmysqlserver -e MYSQL_ROOT_PASSWORD=mysql@root_pw -p 33306:3306 -d mysql:8
docker exec -it testmysqlserver /bin/bash
