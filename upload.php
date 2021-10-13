<?php
   define('DB_SERVER', 'localhost');
   define('DB_USERNAME', 'lohran.bentemuller');
   define('DB_PASSWORD', 'B1scoitinho');
   define('DB_DATABASE', 'CFO');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE) ;
   if(mysqli_connect_errno()) {
    die("Falha de conexao com banco de dados " .mysqli_connect_error());
    }

$sql = "select * from TCO where contador=".$_GET['id'];
$result=mysqli_query($db,$sql);
$row=mysqli_fetch_array($result,MYSQLI_ASSOC);
$id_TCO=$row['id'];
 

$ds          = DIRECTORY_SEPARATOR;  //1
 
$storeFolder = 'uploads/';   //2
 
if (!empty($_FILES)) {
     //$sql="insert into anexo_TCO(id_TCO,caminho) values(".$_GET['id'].",'".$storeFolder."/".$_FILES['file']['tmp_name']."')";
	 //$result=mysqli_query($db,$sql);
    //$sql="insert into anexo_TCO (caminho,contador) values ('".$storeFolder."/".$_FILES['file']['tmp_name']."',".$_GET['id'].")";
	//$sql="insert into anexo_TCO (caminho,contador) values ('".$storeFolder."/".explode(".",$_FILES['file']['name'])[0]."_".date('Y-m-d H:i:s').".".explode(".",$_FILES['file']['name'])[1]."',".$_GET['id'].")";
    //$result=mysqli_query($db,$sql); 
	
    $tempFile = $_FILES['file']['tmp_name'];          //3             
      
    $targetPath = dirname( __FILE__ ) . $ds. $storeFolder . $ds;  //4
     
    //$targetFile =  $targetPath. $_FILES['file']['name']."_".date('Y-m-d H:i:s');  //5
	$targetFile= $targetPath. explode(".",$_FILES['file']['name'])[0]."_".date('Y-m-d H:i:s').".".explode(".",$_FILES['file']['name'])[1];
 
    move_uploaded_file($tempFile,$targetFile); //6


}
?>     