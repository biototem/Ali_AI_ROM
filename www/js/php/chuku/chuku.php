<?php
session_start();
require "../../extr/db_connect.php";

// echo "aaa";
var_dump($_REQUEST);

$ks = addslashes($_GET['ks']);

$ys = addslashes($_GET['ys']);

$cm = addslashes($_GET['cm']);

$sl = addslashes($_GET['sl']);

$sql = "update `kc` set `$cm`=`$cm`-$sl where `ks` = '$ks' and `ys` = '$ys' ";
$sql_info = "insert into `info`(ks,ys,cm,sl,czx,czr) value('$ks','$ys','$cm',$sl,'出库','".$_SESSION['user']."')";
$flag = false;
try {
    $db->execSql($sql);
    $db->execSql($sql_info);
    $flag = true;
} catch (Exception $e) {
     $a = $e->getMessage();
}

if($flag){
    echo "
    <script>
        alert('商品出库成功');
        window.location.href='../../web/show/show.html';
    </script>
    ";
}else{
    echo "
    <script>
        alert('出库失败，检查是否输入有误，请重新输入!!');
        window.location.href='../../web/chuku/chuku.php';
    </script>
    ";
}