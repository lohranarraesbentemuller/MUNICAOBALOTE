<?php
   if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

 //print_r($_SESSION);exit("TESTE");
   $user_check = $_SESSION['login_user'];
   $sql2="select * from login where nome = '".$user_check."' ";
   $ses_sql = mysqli_query($db,$sql2);
   //echo $sql2;
   $row = mysqli_fetch_array($ses_sql,MYSQLI_ASSOC);

   $login_session = $row['nome'];

 $caminho=$_SERVER['REQUEST_URI'];
 $papeis=explode("|",$_SESSION['papel']);
 
  $sql="select * from login_esfo where id_login=".$row['id'];
  //echo $sql;
 // exit();
  $result=mysqli_query($db,$sql);
  $row=mysqli_fetch_array($result,MYSQLI_ASSOC);
  
  $antiguidade=$row['matricula_esfo'];

 if(!isset($_SESSION['login_user'])){
      header("location:login.php");
	  //echo "<script type='text/javascript'>window.top.location='login.php';</script>"; //exit;
  }

//if(count(explode("roubados.php",$caminho))>1)
//{
	if(strtoupper($user_check)=='LOHRAN.BENTEMULLER' || strtoupper($user_check)=='JOSE.FARIAS')
	  {}
	else
		//echo "<script type='text/javascript'>window.top.location='login.php';</script>";
	    header("location:login.php");
//}
//teste

 

//teste 

 
 if(!(in_array("Administrador",$papeis) || in_array("Escalante",$papeis)))
 {
 if(count(explode('graficos.php',$caminho))>1)//se estou na pagina graficos.php
 {
	 //echo 'graficos.php?antiguidade='.$antiguidade;
	 //exit();
	 if($caminho!='/ESCALA/graficos.php?antiguidade='.$antiguidade)
		 header('location:graficos.php?antiguidade='.$antiguidade);	 
		 //echo "<script type='text/javascript'>window.top.location='graficos.php?antiguidade='".$antiguidade.";</script>"; exit;
		 //header('location:graficos.php?antiguidade='.$antiguidade);	 
 }
 else
 {
   	
 
 if(count(explode('ver_escala.php',$caminho))==1) //se nao eh a pagina ver_escala
 {
	 //if ($_SESSION['papel']!='Administrador')
		 if(in_array("Administrador",$papeis) || in_array("Escalante",$papeis)) 
	     {
		   echo "OK";
	     }
		 else{  //se vc nao eh adminsitrador ou escalante
		    if(count(explode("baixados_visualizar.php",$caminho))>1)
			{
				
			}
			else{
			//	echo $caminho;
				//exit();
			 print_r($papeis);
		//echo "<script type='text/javascript'>window.top.location='ver_escala.php'</script>"; exit;
		 header("location:getTop.php");
		 }
		 }
 }
}
 }
?>