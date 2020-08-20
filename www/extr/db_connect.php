<?php
    header("Content-type:text/html;charset:utf-8");

    // require "pdo.php";

    // $db = mypdo::getInstance('192.168.3.188:33306', 'developer', '3rhva5', 'ai_rom', 'utf8');

    $dbHost = '192.168.3.188:33306';
    $dbName = 'ai_rom';
    $user = 'developer';
    $pass = '3rhva5';

    try {
        $dsn = 'mysql:host='.$dbHost.';dbname='.$dbName;
        $dbh = new PDO($dsn, $user, $pass);
        echo '链接成功';
    } catch (PDOException $e) {
        print "Error!: " . $e->getMessage() . "<br/>";
        die();
    }
?>