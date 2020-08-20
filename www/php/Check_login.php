<?php 
session_start();
header("Content-type:text/html;charset=utf-8");

if(!isset($_SESSION['user_account'])){
	echo "<script>alert('请先登录！');window.location.href='../web/Login.php';</script>";
	exit();
}

?>