<?php
session_start();
require "../../extr/db_connect.php";

// var_dump($_GET);


$ks = addslashes($_GET['ks']);

$ys = addslashes($_GET['ys']);

$cm = addslashes($_GET['cm']);

$sl = $_GET['sl'];

$sql_kc = "update `kc` set `$cm`=`$cm`+$sl where `ks` = '$ks' and `ys` = '$ys' ";
$sql_info = "insert into `info`(ks,ys,cm,sl,czx,czr) value('$ks','$ys','$cm',$sl,'入库','".$_SESSION['user']."')";
$flag = false;
// 进行事务处理
$db->beginTransaction();
try {
    $db->execSql($sql_kc);
    $db->execSql($sql_info);
    $flag = true;
} catch (Exception $e) {    
    $a = $e->getMessage();
}
$db->commit();

if($flag){
    echo "
    <script>
        alert('商品入库成功');
        window.location.href='../../web/show/show.html';
    </script>
    ";
}else{
    echo "
    <script>
        alert('入库失败，检查是否输入有误，请重新输入!!');
        window.location.href='../../web/ruku/ruku.html';
    </script>
    ";
}