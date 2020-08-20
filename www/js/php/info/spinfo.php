<?php
require_once '../../extr/db_connect.php';

$sql = "select * from ks where is_del=0";

$result = $db->query($sql);

echo json_encode($result);