<?php
require_once '../../extr/db_connect.php';

$sql = "select * from info";

$result = $db->query($sql);

echo json_encode($result);