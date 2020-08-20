<?php

    $conn = mysqli_connect('192.168.3.188', 'developer', '3rhva5', 'ai_rom', '33306');
    if(!$conn) {
        echo mysqli_connect_error();
    }else{
        echo "Connected successfully";
    }
	$result = $conn->query('select user_account, user_pwd from ai_rom.user_info;');
	echo $result->num_rows;
?>

<!-- 
insert ai_rom.user_info(user_account,user_pwd,user_class,register_time)
values ('test2', MD5('test2'), 1,'2020-08-13');

update ai_rom.user_info
set user_pwd=md5('test2')
where user_account = 'test2';


select user_account, user_pwd
from ai_rom.user_info;
 -->
