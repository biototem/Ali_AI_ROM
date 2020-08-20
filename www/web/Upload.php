<?php 
    // require_once '../php/Check_login.php';
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>上传文件</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
    <script language="javascript">
	function  F_submit(){
		document.upload.target="_blank";
		document.upload.action="http://192.168.3.188:8000/upload_img";
		document.upload.submit();
		document.upload.target="_blank";
		document.upload.action="../php/Upload.php";
		document.upload.submit();
		}
	</script>
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
    
	<h2>上传文件</h2>
	<form name='upload' action="" method="post" enctype="multipart/form-data" style="text-align:center">
		<input type="file" name="file" id="file">
		<input type="text" name="task_type" id="text2">
		<input type="button" name="Submit" value="提交" onClick="F_submit()">
	</form>

	<form name='get_task_result' action="../php/post_task_result.php" method="post" enctype="multipart/form-data" style="text-align:center">
		<label>filename</label>
		<input type="text" name="filename" id="text2">
		<label>user_id</label>
		<input type="text" name="user_id" id="text2">
		<input type="submit" name="Submit" value="提交">
	</form>
</html>