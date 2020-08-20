<?php 
    require_once '../php/Check_login.php';
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>创建任务</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
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
		<h2>创建任务类型</h2>
		<a href='./Upload.php'>拇指桡侧外展测量</a><br>
		<a href='./Upload.php'>肩关节外展测量</a><br>
	</div>
</html>