<?php
	session_start();    //启动会话
	session_unset();    //删除会话
	session_destroy();  //结束会话
	echo "<script>window.location.href='../../web/Login.php';</script>"
?>