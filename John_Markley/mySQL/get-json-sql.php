<?php
    $username = "jarvisreadonlyuser"; 
    $password = "password";   
    $host = "localhost";
    $database="jarvis";
    
    $server = mysql_connect($host, $username, $password);
    $connection = mysql_select_db($database, $server);

//data it the 
    $myquery = "
SELECT `sensorDateTime`, `sensorValue` FROM  `sensorLogs`
";


    $query = mysql_query($myquery);
    
    if ( ! $query ) {
        echo mysql_error();
        die;
    }
    
    $data = array();
    
    for ($x = 0; $x < mysql_num_rows($query); $x++) {
        $data[] = mysql_fetch_assoc($query);
    }
    
    
    
    echo json_encode($data); // prints the array in json formatting
     
    mysql_close($server);
?>