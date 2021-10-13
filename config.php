<?php
   define('DB_SERVER', 'localhost');
   define('DB_USERNAME', 'USUARIO_DB');
   define('DB_PASSWORD', 'SENHA_DB');
   define('DB_DATABASE', 'DB');
  // mysql_query("SET NAMES utf8");
  // mysql_query("SET CHARACTER SET utf8");

   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE) ;
   if(mysqli_connect_errno()) {

    die("Falha de conexao com banco de dados " .mysqli_connect_error());

    }

?>