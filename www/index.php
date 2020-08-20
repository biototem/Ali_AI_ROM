<?php 
require_once './php/Check_login.php';
?>


<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>关节活动度智能测量康复评定平台</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
    <!-- <script src="main.js"></script> -->
</head>

<body>
    <div id="header" style="background:rgb(78,238,148);">
        <br/>
		<h1 style="text-align:center">关节活动度智能测量康复评定平台</h1>
	</div>
    <div id="content">
        <div id="left_menu" style="background:rgb(127,255,212);">
            <ul>
                <li><a href="./web/TASK_INFO.php" target="main">用户任务列表</a></li>
            </ul>
            
            <ul>
                <li><a href="./web/CREATE_TASK.php" target="main">创建任务</a></li>
            </ul>

            <ul>
                <li><a href="./web/Password_Manage.php" target="main">密码管理</a></li>
            </ul>

            <ul>
                <li><a href="./php/Exit.php" target="_parent">退出系统</a></li>
            </ul>

        </div>

        <div id="right_main">
            <iframe id="iframe" width="100%" height="100%" marginheight="0" marginwidth="0" hspeace="0" vspace="0"
                frameborder="0" scrolling="auto" seamless src="./web/TASK_INFO.php" name="main">
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
                </head>
            </iframe>
        </div>
    </div>
</body>

</html>