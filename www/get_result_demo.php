<!DOCTYPE html>
<html lang='en'>
<head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=0'/>
    <title>生物图腾 - 关节活动度智能测量康复评定平台</title>
    	    <link rel='stylesheet' href='css/linecons.css' type='text/css'>
    		    <link rel='stylesheet' href='css/font-awesome.min.css' type='text/css'>
    		    <link rel='stylesheet' href='css/bootstrap.css?v=5' type='text/css'>
    		    <link rel='stylesheet' href='css/xenon-core.css?v=5' type='text/css'>
    		    <link rel='stylesheet' href='css/xenon-forms.css' type='text/css'>
    		    <link rel='stylesheet' href='css/xenon-components.css' type='text/css'>
    		    <link rel='stylesheet' href='css/xenon-skins.css' type='text/css'>
    		    <link rel='stylesheet' href='css/custom.css' type='text/css'>
    	
    	       <script src='js/jquery-1.11.1.min.js'></script>
    	    <style type='text/css'>
        .font-before{
            font-size:18px;
            color: #D7D8D7;
            font-weight: bold;
        }
        .font-after{
            font-size:18px;
            color: #797579;
            font-weight: bold;
        }
        .font-choose{
            font-size:18px;
            color: #363636;
            font-weight: bold;
        }
        .form-style{
            margin-left: 55px;
            margin-bottom: 25px;
        }
        .tianchong{
            width: 180px;
            height: 50px;
            padding: 0;
            border: none;
            background-image: url(img/tianchong.png);
            font-size:16px;
            color: #363636;
        }
        .queding{
            width: 90px;
            height: 50px;
            padding: 0;
            border: none;
            background-image: url(img/queding.png);
            margin-left: 10px;
            font-size:16px;
            color: #363636;
        }
        .loukong{
            width: 360px;
            height: 50px;
            padding: 0;
            border: none;
            background-color: #fff;
            background-image: url(img/loukong_new.png);
            font-size:16px;
            color: #363636;
        }
        .span-style{
            font-size:20px;
            color: #114B8E;
            font-weight: bold;
            float: right;
            width: 30%;
        }
        .span-style-modify{
            font-size:18px;
            color: #b4b4b4;
            float: right;
            width: 30%;
            cursor:pointer;
            display: none;
        }
        .submit-style{
            width: 200px;
            height: 50px;
            padding: 0;
            border: none;
            background-image: url(img/submit1.png);
            font-size:22px;
            color: #fff;
        }
        .submit-style2{
            width: 200px;
            height: 50px;
            padding: 0;
            border: none;
            background-image: url(img/submit2.png);
            font-size:22px;
            color: #797579;
        }
    </style>
</head>

<body class='page-body' style='font-family: Regular'>
    <?php
        session_start();        
		if(!isset($_SESSION['user_id'])){
            echo "<script>alert('无未完成任务，请先上传任务！');
            window.location.href='upload_demo.html';</script>";
        }
	echo "
<div class='page-container settings-pane-close'>

    <div style='background: #eee;width: 200px;' class='sidebar-menu toggle-others fixed'>
        <div class='sidebar-menu-inner'>
            <header style='height: 64px;border-bottom: none;' class='logo-env'>
                <!-- logo -->
                <div class='logo'>
                    <a href='#' class='logo-expanded'>
                        <img src='img/logo3.png' width='124px' height='28px' style='margin-top:-9px' alt='关节活动度检测平台'/>
                    </a>
                </div>
            </header>

			
            <ul id='main-menu' style='padding: 0;margin: 0;'>
				<li style='height:46px;text-align: center;'>
                    <a style='line-height: 46px;display:inline-block;' href='upload_demo.html' class='post_op' title='创建任务'>
                        <span style='font-size:16px;color: #777777;' class='title'>创建任务</span>
                    </a>
                </li>
				<li style='background-color: #F9F9F9;height:46px;text-align: center;-moz-box-shadow:0px 5px 5px #DCDCDC; -webkit-box-shadow:0px 5px 5px #DCDCDC; box-shadow:0px 5px 5px #DCDCDC;' class='opened active'>
                    <a style='line-height: 46px;display:inline-block;' href='#' title='查看测量结果'>
                        <span style='font-size:16px;color: #2B2B2B;font-weight: bold;' class='title'>查看测量结果</span>
                    </a>
                </li>

            </ul>

        </div>
    </div>

    <div class='main-content' style='padding: 0;'>

        <nav style='position: relative;z-index: 1;background-color: #fff;height: 64px;-moz-box-shadow:0px 5px 5px #DCDCDC; -webkit-box-shadow:0px 5px 5px #DCDCDC; box-shadow:0px 5px 5px #DCDCDC;' class='' role='navigation'>
            <!-- Left links for user info navbar -->
            <ul style='margin: 0;height: 64px;' class='user-info-menu left-links list-unstyled'>
                <li style='float: left;text-align: center;margin-left: 41px;' class='hidden-sm hidden-xs'>
                    <a style='line-height: 64px;display:inline-block;'>
                        <span style='font-size:22px;color: #383838;font-weight: bold;' class='title'>生物图腾 - 关节活动度智能测量康复评定平台</span>
                    </a>
                </li>
            </ul>
        </nav>	";
		
        $user_id = $_SESSION["user_id"];
        $root_dir = $_SESSION["root_dir"];
        $task_id = $_SESSION["task_type"];
        $filename = $_SESSION["filename"];


        $url = 'http://192.168.3.188:8000/det/'.$filename;
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//设置是否返回信息
        $response = curl_exec($ch);//接收返回信息
        curl_close($ch); //关闭curl链接

        $result = json_decode($response);
		echo '<form name="show" style="text-align:left">';
		echo '<div style= "background: #fff;padding-bottom: 20px;">';
		echo '<div class="panel panel-default">';
		echo '<div class="panel-body" id="main">';
        if ($result->{'msg'}=='success'){
					
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

			$whole_max_angle = $result->{'result'}->{'max_angle'};
			$whole_max_angle = sprintf("%.1f",$whole_max_angle);
			$whole_min_angle = $result->{'result'}->{'min_angle'};
			$whole_diff_angle = $result->{'result'}->{'max_diff_angle'};				
			$whole_min_angle = sprintf("%.1f",$whole_min_angle);
			$whole_diff_angle = sprintf("%.1f",$whole_diff_angle);				
            // if(curl_errno($ch)){//出错则显示错误信息
            //     echo curl_error($ch);
            // }
		
				
			if ($task_id==1){
				$class_title = '正面右肩关节外展测量结果';
			} elseif ($task_id==2) {
				$class_title = '拇指桡侧关节外展测量结果';
			}
			elseif ($task_id==3) {
				$class_title = '拇指掌腕关节伸直测量';
			}
			elseif ($task_id==4) {
				$class_title = '拇指掌腕关节屈曲测量';
			}
			elseif ($task_id==5) {
				$class_title = '拇指掌腕关节外展测量';
			}
			elseif ($task_id==6) {
				$class_title = '拇指掌指关节屈曲伸直测量';
			}
			elseif ($task_id==7) {
				$class_title = '拇指指间关节屈曲伸直测量';
			}

			echo "<div class='form-group form-style'>
			<label class='control-label font-choose'>$class_title<br/></label>";
			if ($extension == 'mkv' || $extension== 'mp4' ){				
				echo "<div class='col-sm-3' style='padding-right: 900px; float: right'><video object-fit:fill width='565' height='754' controls autoplay loop>
				<source src= $img_result_path>
				分析结果以视频形式展示，但您的浏览器不支持 HTML5 video 标签。
				</video>
				</div>";
				echo "<div class='form-group form-style'>";
				echo "<p style='font-size: 16px;color: #383838;'><br/>最大角度是 $whole_max_angle<br/><br/>最小角度是 $whole_min_angle<br/><br/>最大关节活动度是 $whole_diff_angle </p></label>";
				echo '</div>';
			} else {
					$img_info = getimagesize($img_result_path);
					$img_width = $img_info[0];
					$img_height = $img_info[1];
					if ($img_width + $img_height >=1700){
						$img_width = $img_width /2;
						$img_height = $img_height /2;
					}
					//echo '<div class="form-group form-style">';
					//echo '<label class="control-label font-choose">测量角度是$whole_max_angle <br/></label>';
					echo "<p style='font-size: 16px;color: #383838;'><br/>测量角度是$whole_max_angle <br/></p>";
					//echo '</div>';
					echo "<div style='text-align:center'><img width=$img_width height=$img_height src=$img_result_path></div></div>";
					echo "<p><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></p>";
					}
            session_unset();
            session_destroy();            
        } else {
			echo "<div class='form-group form-style'>
				  <label class='control-label font-choose'><br/><br/>分析进行中，如果图片较大或者是视频文件，分析需时最长数分钟，稍后会自动刷新，请勿离开页面<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></label>
                  </div></div>
				  <META HTTP-EQUIV= REFRESH CONTENT='60;URL=get_result_demo.php'>
				  ";
				  
            //echo "<p style='text-align:center'><br/><br/>分析进行中，因视频文件上传耗时，分析需时数分钟，请稍后刷新重试！！！</p>";
        }
			echo "</div>
			</div>
			</div>
			</form>";
    ?>
			
<div style='clear:both'></div>
<footer class='main-footer sticky footer-type-1' style='margin: 0;'>
    <div class='footer-inner'>

        <div class='footer-text'>
            &copy; 2017
            <strong>Bio-Totem 佛山生物图腾科技有限公司</strong>
            <a href='http://www.bio-totem.com/' target='_blank' title='生物图腾'>http://www.bio-totem.com/</a>
        </div>
    </div>
</footer>
<div id='footerWrap'></div>

<div class='modal' id='modal-main'></div>
</div>
<div id='footerWrap'></div>

<div class='modal' id='modal-main'></div>
</body>
</html>
