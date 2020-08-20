<?php
require_once '../../extr/db_connect.php';

$sql = "select kc.* from kc join ks on kc.ks = ks.ks and ks.is_del=0";
// echo $sql;

$result = $db->query($sql);

echo json_encode($result);