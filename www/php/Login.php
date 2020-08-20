<?php
session_start();
require_once '../extr/db_connect.php';

// var_dump($_GET);


$user_account = $_POST['user_account'];
$user_pwd = $_POST['user_pwd'];

$sql="SELECT * FROM `user_info` WHERE `user_account` = :user_account AND `user_pwd` = MD5(:user_pwd)";
$sth = $dbh->prepare($sql);
$sth->bindParam(':user_account', $user_account, PDO::PARAM_STR);
$sth->bindParam(':user_pwd', $user_pwd, PDO::PARAM_STR);
$sth->execute();
$count = $sth->rowCount();

echo $sth->queryString;

// // 进行事务处理
// $db->beginTransaction();
// try {
//     $result=$db->query($sql,'Row');
// } catch (Exception $e) {    
//     $a = $e->getMessage();
// }
// $db->commit();

// echo $count;
// if( $count==1 ){
// 	$_SESSION['user_account']=$user_account;
// 	$_SESSION['user_pwd']=$user_pwd;
//     echo "
//     <script>
//         alert('登录成功');
//         window.location.href='../index.php';
//     </script>
//     ";
// }else{
//     echo "
//     <script>
//         alert('用户名或密码错误,请重新登录!');
//         window.location.href='../web/Login.php';;
//     </script>
//     ";
// }
?>