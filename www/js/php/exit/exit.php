<?php
	session_start();    //�����Ự
	session_unset();    //ɾ���Ự
	session_destroy();  //�����Ự
	echo "<script>window.location.href='../../web/Login.php';</script>"
?>