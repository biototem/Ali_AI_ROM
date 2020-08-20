<?php 
    require_once '../php/Check_login.php';
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>密码管理</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../css/main.css" />
    <!-- <script src="main.js"></script> -->
</head>

<body>
	<?php 
		if($_SESSION['qx']=='1'){
			echo "
				<p>".$_SESSION['user'].",您好！</p>";
		}else{
			echo "
				<p>".$_SESSION['user'].",您好！</p>";
		}
	?>
	
	<div id='main' style='text-align: center;'>
		<h2>密码管理</h2>
		<a href=''>修改密码</a><br>
		<a href=''>忘记密码</a><br>
	</div>
</html>