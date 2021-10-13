<?php
include("config.php");
include("session.php");
//echo "teste";
//$command=escapeshellcmd("screen -m -d python3.6 /home/wwcfo2/www/MUNICAO_BALOTE/src/core4.py");
$command=escapeshellcmd("killall python3.6"); 
$output = shell_exec($command);
$command=escapeshellcmd(" python3.6 ./src/core4.py"); 
//echo $command;
echo "BOT REINICIADO, FAVOR FECHAR A JANELA";
$output = shell_exec($command);
 
 
?>