<?php

define('DB_SERVER', 'localhost');
   define('DB_USERNAME', 'USUARIO_DB');
   define('DB_PASSWORD', 'SENHA_DB');
   define('DB_DATABASE', 'DB');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
   if(mysqli_connect_errno()) {

    die("Falha de conexao com banco de dados " .mysqli_connect_error());

    }
	
	$lat= $_GET['lat'];
	$lng= $_GET['lng'];
	$id= $_GET['id'];
	$placa=$_GET['placa'];
	$sql="delete from localizacao_balote where identificacao='".$id."'";
//	$result=mysqli_query($db,$sql);
	//echo $sql;
//	echo "<BR>";
    $sql="select * from roubados where tudo like '%". substr($placa, 0, 3)."".substr($placa, -4)."%' union all select * from roubados where tudo like '%".substr($placa, 0, 3)." ".substr($placa, -4)."%' union all select * from roubados where tudo like '%".substr($placa, 0, 3)."-".substr($placa, -4)."%'";
	//$sql="insert into localizacao_balote(identificacao,lat,lng,data) values('".$id."','".$lat."','".$lng."',now(),'".$_GET['placa'])."'";
    $result=mysqli_query($db,$sql);
 	//echo $sql;
	//print_r($result);
    if(mysqli_num_rows($result)>0)
	{
		echo  '{"data":[{"id":"22352","resultado":"Possivel produto de roubo/furto"}]}';
	}
	else
	{
	   echo '{"data":[{"id":"22352","resultado":"Sem restrições"}]}';
	}
?>