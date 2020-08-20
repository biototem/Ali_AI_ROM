<?php
	session_start(); 
	$_SESSION["user_id"] = 	"test";
	$_SESSION["task_type"] = $_POST["task_type"];
	$_SESSION["root_dir"] = "Upload/";

	$user_id = $_SESSION['user_id'];
	$root_dir = $_SESSION["root_dir"];
	$task_id = $_SESSION["task_type"];

	$temp = explode(".", $_FILES["file"]["name"]);
	$extension = end($temp);     // 获取文件后缀名
	if (!file_exists($root_dir.$task_id)){
		mkdir($root_dir.$task_id);
	}
	$save_name = $user_id.time().'.'.$extension;
	$img_path = $root_dir.$task_id.'/'.$save_name;

	$allowedExts = array("jpg", "png", "bmp", "mkv", "mp4");
	if (in_array($extension, $allowedExts)){
		move_uploaded_file($_FILES["file"]["tmp_name"],  $img_path);
		$cfile = new CURLFile($img_path, $_FILES["file"]["type"], $save_name);
	} else {
		session_unset();
		session_destroy(); 
		echo "
		<script>
			alert('非法文件格式,请上传jpg, png, bmp, mkv, mp4文件重新创建任务！！！');
			window.location.href='upload_demo.html';
		</script>
		";	
	}

	// 上传至接口
	$url = "http://192.168.3.188:8000/upload_img";
	$post_data = array();
	$post_data["file"] = $cfile;
	$post_data["task_type"] = $task_id;
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//设置返回信息
	curl_setopt($ch, CURLOPT_TIMEOUT, 60);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
	$response = curl_exec($ch);

	$response = json_decode($response);
	if ($response->{"msg"} == "success"){
		$_SESSION["filename"] = $response->{"filename"};
		echo "
		<script>
			alert('上传成功,点击继续查看结果！！！');
			window.location.href='get_result_demo.php';
		</script>
		";	
	} else {
		session_unset();
		session_destroy(); 
		echo "
		<script>
			alert('上传失败,请重新创建任务！！！');
			// window.location.href='upload_demo.html';
		</script>
		";	
	}
?>
