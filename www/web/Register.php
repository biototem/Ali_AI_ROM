<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>用户注册</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
</head>

<body>
    <div id="header" style="background:rgb(78,238,148);">
        <br />
        <h1 style="text-align:center">关节活动度智能测量康复评定平台</h1>
    </div>
    <h2>用户注册</h2>
    <form action="../php/Register.php" method="GET" style="text-align:center">
        <label>用户名称</label>
        <input type="text" name="user" id="user"><br>

        <label>用户密码</label>
        <input type="password" name="pw" id="pw"><br>

        <label for="male">选择权限</label>
        <input type="radio" id="root" name="qx" value='1' />医生
        <input type="radio" id="user" name="qx" value='2' />普通用户<br>

        <input type="submit" value="提交">
    </form>
</body>

</html>