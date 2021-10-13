<?php
include("config.php");
include("session.php");
include('../FO/config.php');
//require( 'ssp.class.php' );
require( '../FO/ssp.class.php' );		  
$sql_details = array(
    'user' => 'lohran.bentemuller',
    'pass' => 'B1scoitinho',
    'db'   => 'CFO',
    'host' => 'localhost'
);
 
$columns = array(
    array( 'db' => 'id', 'dt' => 'id' ),
    array( 'db' => 'nome','dt' => 'nome'),
	array( 'db' => 'mensagem','dt' => 'mensagem'),
    array( 'db' => 'resposta','dt' => 'resposta'),
    array( 'db' => 'data','dt' => 'data'),
	
);

$table = <<<EOT
 (
  select t1.id,nome,mensagem,resposta,data from(select * from balote_auditoria)t1 inner join (select * from cadastro_balote) t2 on t1.id_telegram=t2.id_telegram order by data desc
 ) temp
EOT;

$primaryKey='id';
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
