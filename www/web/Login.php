<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>登录</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
</head>
<body>
    <div id="header" style="background:rgb(78,238,148);">
        <br/>
		<h1 style="text-align:center">关节活动度智能测量康复评定平台</h1>
	</div>
    <h2>登录</h2>
    <form method="POST" action="../../php/Login.php" style="text-align:center">
        <label>用户名称</label>
        <input type="text" name="user_account"><br>
        <label>用户密码</label>
        <input type="password" name="user_pwd"><br>
        <a href=''>忘记密码？</a>
        <a href='../Web/Register.php'>未注册？</a><br>
        <input type="submit" value="提交">
    </form>
    <a href='../check.php'>检查数据库链接</a><br>
    <a href="./Upload.php" target="main">上传文件</a>
</body>
</html>