<?php
    $root_dir = '/media/totem/Cjh/Upload/';

    $filename = $_POST['filename'];
    $user_id = $_POST['user_id'];

    $url = 'http://192.168.3.188:8000/det/'.$filename;
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//设置是否返回信息
    $response = curl_exec($ch);//接收返回信息

    if(curl_errno($ch)){//出错则显示错误信息
        echo curl_error($ch);
    }

    curl_close($ch); //关闭curl链接
    // $result = json_decode($response);
    
    $result = json_decode($response);
    $task_id = $result->{"result"}->{"det_type"};

    $json_path = $root_dir.$task_id.'/'.$user_id.time().'_result.txt';
    file_put_contents($json_path, $response); //保存文件
    
    if ($result->{'msg'}=='success'){

        $url = "http://192.168.3.188:8000/det/".$filename."?only_draw=1";
        // $url = 'http://192.168.3.188:8000/det/'.$filename;
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//设置是否返回信息
        $response = curl_exec($ch);//接收返回信息

        if(curl_errno($ch)){//出错则显示错误信息
            echo curl_error($ch);
        }
        echo gettype($response);
        echo "<img src=$url>";
    } else {
        echo "分析进行中";
    }

?>