<?php
session_start();
require_once '../extr/db_connect.php';

// var_dump($_GET);


$user=$_POST['user'];
$pw=$_POST['pw'];

$sql="select * from user where user='$user' and pw='$pw'";

// 进行事务处理
$db->beginTransaction();
try {
    $result=$db->query($sql,'Row');
} catch (Exception $e) {    
    $a = $e->getMessage();
}
$db->commit();

if($result!=null){
	$_SESSION['user']=$result['user'];
	$_SESSION['qx']=$result['qx'];
    echo "
    <script>
        alert('登录成功');
        window.location.href='../index.php';
    </script>
    ";
}else{
    echo "
    <script>
        alert('用户名或密码错误,请重新登录!');
        window.location.href='../web/Login.php';;
    </script>
    ";
}