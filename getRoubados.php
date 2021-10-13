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
	array( 'db' => 'batalhao','dt' => 'batalhao'),
	array( 'db' => 'total','dt' => 'total'),
    //array( 'db' => 'resposta','dt' => 'resposta'),
    //array( 'db' => 'data','dt' => 'data'),
	
);

$table = <<<EOT
 (
   select nome,batalhao,count(nome) as total from (select * from cadastro_balote)t1 left join (select * from balote_auditoria) t2 on t1.id_telegram=t2.id_telegram group by nome

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
