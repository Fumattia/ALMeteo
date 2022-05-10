// Code Written by Rishi Tiwari
// Website:- https://tricksumo.com
// Reference:- https://www.w3schools.com/php/php_mysql_insert.asp
//
//

<?php



    $host = "localhost";		         // host = localhost because database hosted on the same server where PHP files are hosted
    $dbname = "ALMeteo";              // Database name
    $username = "user";		// Database username
    $password = "password";	        // Database password


// Establish connection to MySQL database
$conn = new mysqli($host, $username, $password, $dbname);


// Check if connection established successfully
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

else { echo "Connected to mysql database. "; }

   
// Get date and time variables
    date_default_timezone_set('Europe/Rome');  // for other timezones, refer:- https://www.php.net/manual/en/timezones.asia.php
    $d = date("Y-m-d");
    $t = date("H:i:s");
    
// If values send by NodeMCU are not empty then insert into MySQL database table

  if(!empty($_POST['tabella']))
    {
		$tab = $_POST['tabella'];
                $temp = $_POST['sendtemp'];
				$hum = $_POST['sendhum'];
				$pres = $_POST['sendpres'];
				$qaria = $_POST['sendqaria'];
				$pioggia = $_POST['sendpioggia'];
				


// Update your tablename here
	        $sql = "INSERT INTO `ALMeteo`.`".$tab$"` (`Temperatura`, `Umidita`, `Pressione`, `Q_aria`, `Pioggia`, `Data`, `Ora`) VALUES ('".temp."','".$hum."', '".$pres."', '".$qaria."', '".$pioggia."', '".$d."', '".$t."')"; 
 


		if ($conn->query($sql) === TRUE) {
		    echo "Values inserted in MySQL database table.";
		} else {
		    echo "Error: " . $sql . "<br>" . $conn->error;
		}
	}


// Close MySQL connection
$conn->close();



?>
