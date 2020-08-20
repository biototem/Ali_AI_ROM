<?php
header("Content-type:text/html;charset=utf-8");
// 引入pdo
require_once '../../extr/db_connect.php';


$flag = false;

$user = $_GET['user'];
$pw = $_GET['pw'];
$qx = $_GET['qx'];

$arrayDataValue = array(
    'user'=> addslashes($user),
    'pw'=> addslashes($pw),
	'qx'=> addslashes($qx)
);

// 事务开始
$db->beginTransaction();

try {
    // 插入ks表
    $table = "user";
    $db->insert($table,$arrayDataValue);
} catch (Exception $error) {
    $db->rollback();
}
// 提交
$db->commit();

$flag = true;
// var_dump($flag);
if($flag){
    echo "
    <script>
        alert('新增用户成功');
        window.location.href='../../web/show/show.html';
    </script>
    ";
}




