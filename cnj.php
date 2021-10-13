<?php
   define('DB_SERVER', 'localhost');
   define('DB_USERNAME', 'USUARIO_DB');
   define('DB_PASSWORD', 'SENHA_DB');
   define('DB_DATABASE', 'DB');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE) ;
   if(mysqli_connect_errno()) {
    die("Falha de conexao com banco de dados " .mysqli_connect_error());
    }


if($_SERVER["REQUEST_METHOD"] == "POST") {
	
	               //chmod ("uploads/*", 0750);
	            //  $command = escapeshellcmd('/usr/local/bin/python3.6 cnj.py');
                                //echo 'python diario_de_classe.py '.$pelotao.' '.$turma.' '.$_POST['disciplina'];
              //  $output = shell_exec($command);
                  //              echo "<BR>".$output;

	$row = 1;
$sql="delete from mandados_abertos";
$result=mysqli_query($db,$sql);



$files = array();
if ($handle = opendir('./uploads')) {
    while (false !== ($file = readdir($handle))) {
        if ($file != "." && $file != ".." && explode(".",$file)[1]=="csv") {
           $files[filemtime($file)] = $file;
		    
        }
    }
    closedir($handle);

    // sort
    ksort($files);
    // find the last modification
    $reallyLastModified = end($files);
     
    foreach($files as $file) {
        $lastModified = date('F d Y, H:i:s',filemtime($file));
        if(strlen($file)-strpos($file,".swf")== 4){
           if ($file == $reallyLastModified) {
             // do stuff for the real last modified file
			 echo $file;
           }
           echo "<tr><td><input type=\"checkbox\" name=\"box[]\"></td><td><a href=\"$file\" target=\"_blank\">$file</a></td><td>$lastModified</td></tr>";
        }
    }
}





if (($handle = fopen("./uploads/".$reallyLastModified, "r")) !== FALSE) {
  while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
    $num = count($data);
    //echo "<p> $num fields in line $row: <br /></p>\n";
	$row++;
	if($num>5)
	{
     
     //for ($c=0; $c < $num; $c++) {
         //echo $data[$c] . "<br />\n";
		 try{
		 $data_nascimento=explode("/",$data[5])[2]."-".explode("/",$data[5])[1]."-".explode("/",$data[5])[0];
		 }
		 catch(Exception $e)
		 {
		  print_r($e);	 
		 }
		 
		 try{
		 $data1=explode("/",$data[7])[2]."-".explode("/",$data[7])[1]."-".explode("/",$data[7])[0];
		 }
		 catch(Exception $e)
		 {
			 print_r($e);
		 }
		 $aaa='"'.$data[1].'","'.$data[2].'","'.$data[3].'","'.$data[4].'","'.$data_nascimento.'","'.$data[6].'","'.$data1.'","'.$data[8].'","'.$data[9].'"';
		 
		 $sql="insert into mandados_abertos(nome,alcunha,nome_da_mae,nome_do_pai,data_de_nascimento,situacao,data_mandado,orgao,peca) values(".$aaa.");";
		 // echo $sql;
		 $result=mysqli_query($db,$sql);
     //}
	}
  }
  fclose($handle);
}
	               
    #exit('Bot atualizado com sucesso');
}

echo '<script type="text/javascript" language="javascript" src="../jquery-3.6.0.min.js"></script>';
?>
<link rel="stylesheet" href="../jquery-ui-1.12.1/jquery-ui.css">
<link href="../FO/dropzone.css" type="text/css" rel="stylesheet" />
<script src="../dropzone-master/dist/dropzone.js"></script>
<script  src="../ESCALA/jQuery-Mask-Plugin-master/src/jquery.mask.js"></script>
<script type="text/javascript"  src="../jQuery-Autocomplete-master/src/jquery.autocomplete.js"></script>
<script type="text/javascript" src="../roosevelt/arrive-master/src/arrive.js"></script>


<div class="container">

<h1>COMO ATUALIZAR OS MANDADOS DE SEGURANÇA NO MUNIÇÃO BALOTE</h1>

<h7>Acesse <a href="https://portalbnmp.cnj.jus.br/#/pesquisa-peca">https://portalbnmp.cnj.jus.br/#/pesquisa-peca</a></h7>
<h7>em ESTADO selecione DISTRITO FEDERAL</h7>
<img src="tutorial1.JPG"></img>
<h7>Clique em pesquisar, e depois em Exportar, selecione CSV</h7><BR><BR>
<img src="tutorial2.JPG"></img><BR><BR>
<h7>Clique no campo abaixo para fazer upload do arquivo baixado</h7>

<form action="upload.php?id=<?php echo $_GET['id'];?>" class="dropzone dz-clickable"></form>


<form method="post">
<h7>após finalizado o upload, clique nesse <button type="submit">Atualizar mandados</button> o bot estará com a versão mais recente dos mandados de prisão em aberto </h7>
</form>
</div>



<script>
$(document).ready(function(){
$('.dz-message').children('span').each(function()
	 {
 
		 
		 ($(this).html("Arraste o arquivo baixado no portalbnmp aqui"));
		 
	 });
	 
	 
});
</script>