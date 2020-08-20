<?php
$conn=new mysqli('localhost','root','root','mx');
//设定连接编码,目的是和数据库内部的编码一样
$conn->query("set names'utf8'");
//规定当与数据库服务器进行数据传送时要使用的默认字符集
$conn->set_charset('utf8_general_ci');
//把图片保存到服务器指定位置，并且把图片路径插入到数据库中
if($_FILES["file"]["error"]) //file是input上传图片时候的name
{
    echo $_FILES["file"]["error"];
}
else
{
    //控制上传文件的类型，大小
    if(($_FILES["file"]["type"]=="image/jpg" || $_FILES["file"]["type"]=="image/png") && $_FILES["file"]["size"]<1024000)
    {
        //找到文件存放的位置
		//在服务器中新建一个uploads文件夹,图片名中也加入当前时间
        $filename = "uploads/".date("YmdHis").$_FILES["file"]["name"];
         //转换编码格式，只有转换成GB2312，move_uploaded_file函数才不会把图片名字里的中文变成乱码
        $filename1 = iconv("UTF-8","gb2312",$filename);
        //判断文件是否存在
        if(file_exists($filename1))
        {
            echo "该文件已存在！";
        }
        else
        {
            //保存文件，将上传的临时文件移到web服务器中，见《PHP和MySQL web开发》P330
            move_uploaded_file($_FILES["file"]["tmp_name"],$filename1);
            //这里的filename要utf8_general_ci格式,不然和数据库中编码不一致
            $sql="insert into image_test values('".$name."','".$filename."')";
            if($conn->query($sql))
            {
                echo "数据插入数据库";
                }
                else
                {
                    echo "数据未插入数据库";
                    };
        }
    }
    else
    {
        echo "文件类型不正确！";
    }
}

$conn->close();
// $flag = true;
// // var_dump($flag);
// if($flag){
//     echo "
//     <script>
//         alert('新增图片成功');
//         window.location.href='../../web/show/show.html';
//     </script>
//     ";
// }




