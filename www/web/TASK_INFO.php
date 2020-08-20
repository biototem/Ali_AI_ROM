<?php 
    require_once '../php/Check_login.php';
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta http-equiv="refresh" content="60">
    <title>用户任务列表</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
    <!-- <script src="main.js"></script> -->
</head>

<body>
	<?php 
		if($_SESSION['qx']=='1'){
			echo "
				<p>".$_SESSION['user_account'].",您好！</p>";
		}else{
			echo "
				<p>".$_SESSION['user_account'].",您好！</p>";
		}
	?>
    
	<h2>用户任务列表</h2>
	<table border="1">
            <thead>
                <tr>
					<th>任务生成时间</th>  
					<th>任务类型</th>     
					<th>关联医生</th>     
					<th>状态</th>     
                </tr>
            </thead>
            <tbody>
                
            </tbody>
        </table>
</html>