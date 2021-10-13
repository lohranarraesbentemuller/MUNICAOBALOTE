<?php
include("config.php");


//$sql="select * from roubados
$i=$_POST['placa'];
//$i=$_GET['placa'];
//substr(string,start,length)
//$sql = "select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
$sql = "select * from roubados where tudo like '%".substr($i,0,3).substr($i,strlen($i)-4,4)."%' union all select * from roubados where tudo like '%".substr($i,0,3).substr($i,strlen($i)-4,4)."%' union all select * from roubados where tudo like '%".substr($i,0,3).substr($i,strlen($i)-4,4)."%'";
$result=mysqli_query($db,$sql);

echo $sql;
foreach($result as $row){
	echo $row['tudo'];
}
?>