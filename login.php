<?php
if($_SERVER["HTTPS"] != "on")
{
    header("Location: https://" . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"]);
 //   exit();
}
include('config.php'); 
//include('session.php');
if($_SERVER["REQUEST_METHOD"] == "POST") {
 
   $nome=mysqli_real_escape_string($db, $_POST['nome']);
   $password=mysqli_real_escape_string($db, $_POST['senha']);
   
   $nome=utf8_decode($nome);
   $password=utf8_decode($password);
   $sql = "SELECT * FROM login WHERE nome = '".$nome."' and senha = sha2('".$password."',224);";
   //echo $sql;
   $result=mysqli_query($db,$sql);
   //teste
    $row = mysqli_fetch_array($result,MYSQLI_ASSOC);
      $active = $row['id'];
      //echo $sql;
	  //exit();
      $count = mysqli_num_rows($result);
      //echo $count;exit();

      if($count == 1) {
		 session_start();
         $_SESSION['login_user'] = $nome;
         $_SESSION['papel'] = $row['papel'];
		// print_r($_SESSION);echo("lohran");
		 //header("location:ver_escala.php");
		 //print_r( $_SESSION);exit();
		// exit();
		 header("location:index.php"); // exit;
		//echo "<script type='text/javascript'>location='info.php';</script>"; exit();
		//echo "<script type='text/javascript'>location='ver_escala.php';</script>"; exit();
		 
      }else {
         $error = "Your Login Name or Password is invalid"; 
        }
}


?>
<link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script>
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
</script>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<!------ Include the above in your HEAD tag ---------->
<style>
/* Made with love by Mutiullah Samim*/

@import url('https://fonts.googleapis.com/css?family=Numans');

html,body{
//background-image: url('http://getwallpapers.com/wallpaper/full/a/5/d/544750.jpg');
background-image: url('fundo.jpg');
background-size: cover;
background-repeat: no-repeat;
height: 100%;
font-family: 'Numans', sans-serif;
}

.container{
height: 100%;
align-content: center;
}

.card{
height: 370px;
margin-top: auto;
margin-bottom: auto;
width: 400px;
background-color: rgba(0,0,0,0.5) !important;
}

.social_icon span{
font-size: 60px;
margin-left: 10px;
color: #FFC312;
}

.social_icon span:hover{
color: white;
cursor: pointer;
}

.card-header h3{
color: white;
}

.social_icon{
position: absolute;
right: 20px;
top: -45px;
}

.input-group-prepend span{
width: 50px;
background-color: #FFC312;
color: black;
border:0 !important;
}

input:focus{
outline: 0 0 0 0  !important;
box-shadow: 0 0 0 0 !important;

}

.remember{
color: white;
}

.remember input
{
width: 20px;
height: 20px;
margin-left: 15px;
margin-right: 5px;
}

.login_btn{
color: black;
background-color: #FFC312;
width: 100px;
}

.login_btn:hover{
color: black;
background-color: white;
}

.links{
color: white;
}

.links a{
margin-left: 4px;
}
</style>
<!DOCTYPE html>
<html>
<head>
	<title>Login Page</title>
   <!--Made with love by Mutiullah Samim -->
   
	<!--Bootsrap 4 CDN-->
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    
    <!--Fontawesome CDN-->
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">

	<!--Custom styles-->
	<!--<link rel="stylesheet" type="text/css" href="styles.css">-->
</head>
<body>
<div class="container">
	<div class="d-flex justify-content-center h-100">
		<div class="card">
			<div class="card-header">
				<h3>Acessar o site</h3>
				<div class="d-flex justify-content-end social_icon">
					<!--<span><i class="fab fa-facebook-square"></i></span>
					<span><i class="fab fa-google-plus-square"></i></span>
					<span><i class="fab fa-twitter-square"></i></span>-->
				</div>
			</div>
			<div class="card-body">
				<form method="POST">
					<div class="input-group form-group">
						<div class="input-group-prepend">
							<span class="input-group-text"><i class="fas fa-user"></i></span>
						</div>
						<input id="nome" name="nome" type="text" class="form-control" placeholder="usu??rio" autocomplete="off">
						
					</div>
					<div class="input-group form-group">
						<div class="input-group-prepend">
							<span class="input-group-text"><i class="fas fa-key"></i></span>
						</div>
						<input name="senha" type="password" class="form-control" placeholder="senha">
					</div>
					<div class="row align-items-center remember">
						<input type="checkbox">lembrar
					</div>
					<div class="form-group">
						<input type="submit" value="Login" name="login_teste" class="btn float-right login_btn">
					</div>
				</form>
			</div>
			<div class="card-footer">
				<div class="d-flex justify-content-center links">
					N??o possui acesso?<a href="https://wa.me/5561981997618">Solicite um cadastro</a>
				</div>
				<div class="d-flex justify-content-center">
					<a href="email.php">Esqueceu sua senha?</a>
				</div>
			</div>
		</div>
	</div>
</div>
</body>
</html>
