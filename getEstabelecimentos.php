<?php
include("config.php");
include("session.php");
include('../FO/config.php');
//require( 'ssp.class.php' );
require( '../FO/ssp.class.php' );		  
$sql_details = array(
    'user' => 'USUARIO_DB',
    'pass' => 'SENHA_DB',
    'db'   => 'DB',
    'host' => 'localhost'
);
 
$columns = array(
  //  array( 'db' => 'id', 'dt' => 'id' ),
    array( 'db' => 'nome','dt' => 'nome'),
	array( 'db' => 'lat','dt' => 'lat'),
	array( 'db' => 'lng','dt' => 'lng'),
	array( 'db' => 'data','dt' => 'data'),
	array( 'db' => 'placa','dt' => 'placa')
    //array( 'db' => 'resposta','dt' => 'resposta'),
    //array( 'db' => 'data','dt' => 'data'),
	
);

$table = <<<EOT
 (
   select nome,lat,lng,data,placa from (select * from localizacao_balote)t1 inner join (select * from cadastro_balote)t2 on t2.id_telegram=t1.identificacao where placa is not null

 ) temp
EOT;

$primaryKey='nome';
$where="1=1";
//$where=" id_cadete=".$_GET['id_cadete'];
//print_r($_GET);echo "<BR>";
//print_r($sql_details);echo "<BR>";
//print_r($table);echo "<BR>";
//print_r($primaryKey);echo "<BR>";
//print_r($columns);echo "<BR>";
//echo $where."<BR>";
echo json_encode(
    SSP::simple( $_GET, $sql_details, $table, $primaryKey, $columns,$where )
);
//}
       
     ?>
