<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>评定结果</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" media="screen" href="../../css/main.css" />
</head>

<body>
	<div id="header" style="background:rgb(78,238,148);">
		<br />
		<h1 style="text-align:center">生物图腾关节活动度智能测量康复评定平台</h1>
	</div>

    <?php
        session_start();
        if(!isset($_SESSION['user_id'])){
            echo "<script>alert('无未完成任务，请先上传任务！');
            window.location.href='upload_demo.html';</script>";
        }

        $user_id = $_SESSION['user_id'];
        $root_dir = $_SESSION["root_dir"];
        $task_id = $_SESSION["task_type"];
        $filename = $_SESSION["filename"];


        $url = 'http://192.168.3.188:8000/det/'.$filename;
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//设置是否返回信息
        $response = curl_exec($ch);//接收返回信息
        curl_close($ch); //关闭curl链接

        $result = json_decode($response);
        if ($result->{'msg'}=='success'){
		
			if ($task_id==1){
				echo "<h2>拇指桡侧外展测量结果</h2>";
			} elseif ($task_id==2) {
				echo "<h2 style=\"text-align:left\">正面右侧肩关节外展测量结果</h2>";
			}
			
            $temp = explode(".", $filename);
            $extension = end($temp);     // 获取文件后缀名
			
            $json_path = $root_dir.$task_id.'/'.$user_id.time().'_result.txt';
            file_put_contents($json_path, $response); //保存文件

			$url = "http://192.168.3.188:8000/det/".$filename."?only_draw=1";
		
            $ch = curl_init($url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//设置是否返回信息
            $response = curl_exec($ch);//接收返回信息

            $img_result_path = $root_dir.$task_id.'/'.$user_id.time().'_result.'.$extension;
            $img_result = @fopen($img_result_path, 'a');
            fwrite($img_result, $response);
            fclose($img_result);

            // if(curl_errno($ch)){//出错则显示错误信息
            //     echo curl_error($ch);
            // }

			if ($extension == 'mkv' || $extension== 'mp4' ){
				//$info = $result->{'result'};
				$whole_max_angle = $result->{'result'}->{'max_angle'};
				$whole_min_angle = $result->{'result'}->{'min_angle'};
				$whole_max_angle = sprintf("%.1f",$whole_max_angle);
				$whole_min_angle = sprintf("%.1f",$whole_min_angle);
				echo "<h3 style=\"text-align:left\">最大角度是 $whole_max_angle 最小角度是 $whole_min_angle </h3>";
				echo "<div style=\"text-align:center\"> 
				<video object-fit:fill width=\"565\" height=\"754\" controls autoplay loop>
				<source src= $img_result_path>
				分析结果以视频形式展示，但您的浏览器不支持 HTML5 video 标签。
				</video>
				</div>";
			} else {
            echo "<div style='text-align:center'><img src=$img_result_path></div>";
			}
            session_unset();
            session_destroy();            
        } else {
            echo "<p style='text-align:center'>分析进行中，视频文件分析需时数分钟，请稍后刷新重试！！！</p>";
        }

    ?>
    
</html>
