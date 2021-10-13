<?php

/* Getting file name */
$filename = $_FILES['file']['name'];

/* Location */
$location = "uploads/1/".$filename;
$uploadOk = 1;
$uploadOk = 0;
//echo $filename;
$imagens=array();
array_push($imagens,"jpg");
array_push($imagens,"jpeg");
array_push($imagens,"png");
array_push($imagens,"bmp");
//print_r(explode('.',$filename));
//echo sizeof(explode(".",$filename));
$formato=explode(".",$filename)[-1+count(explode(".",$filename))];
//echo $formato;
if(in_array(strtolower($formato),$imagens))
{
	$uploadOk=1;
}

if($uploadOk == 0){
echo 0;
}else{
/* Upload file */
if(move_uploaded_file($_FILES['file']['tmp_name'], $location)){
	echo $location;
}else{
	echo 0;
}
}
?>
