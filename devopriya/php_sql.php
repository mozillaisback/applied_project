<?php

echo "<br";
echo "this is php file";
echo $fileName;
$content = file($fileName);
//echo strtolower($content[0]);

$var_1 = "employee id,employee name,indian phone number,company email id,personal email id,father's name,mother's name,sibling name,reporting boss name,ongoing projects,hobbies,date of birth,recent official visits,leaves availed,leaves remaining,education qualification,institute,type of mobile phone (official),type of mobile phone (personal)";

$var_2 = strtolower(trim($content[0]));



similar_text($var_1, $var_2, $percent);

$serverName = "db-mysql-blr1-82262-do-user-13433417-0.i.db.ondigitalocean.com, 25060";

if ($percent == 100)
{
	echo $percent;
	echo "<br>";
	
	$conn  = new mysqli("db-mysql-blr1-82262-do-user-13433417-0.i.db.ondigitalocean.com:25060","doadmin","AVNS_8JrUC6kgyaIWXPq5GNC","defaultdb");
	// Check connection
	if (!$conn) {
		die("Connection failed: " . mysqli_connect_error());
	}
	echo "<br>";
	echo "Connected successfully";
	echo "<br>";
	echo "<br>";
	$open = fopen($fileName, "r");
	
	$data = fgetcsv($open, 1000, ",");
	
	while (($data = fgetcsv($open, 1000, ",")) !== FALSE) 
	{
	// Read the data    
		//echo "INSERT INTO students (`Employee ID`, `Employee Name`, `Indian Phone Number`, `Company Email ID`, `Personal Email ID`, `Father's Name`, `Mother's Name`, `Sibling Name`, `Reporting Boss Name`, `Ongoing Projects`, `Hobbies`, `Date of Birth`, `Recent Official Visits`, `Leaves Availed`, `Leaves Remaining`, `Education Qualification`, `Institute`, `Type of Mobile Phone (Official)`, `Type of Mobile Phone (Personal)`) VALUES ('$data[0]', '$data[1]', '$data[2]', '$data[3]', '$data[4]', '$data[5]', '$data[6]', '$data[7]', '$data[8]', '$data[9]', '$data[10]', '$data[11]', '$data[12]', '$data[13]', '$data[14]', '$data[15]', '$data[16]', '$data[17]', '$data[18]')";
		$conn->query("INSERT INTO students (`Employee ID`, `Employee Name`, `Indian Phone Number`, `Company Email ID`, `Personal Email ID`, `Father's Name`, `Mother's Name`, `Sibling Name`, `Reporting Boss Name`, `Ongoing Projects`, `Hobbies`, `Date of Birth`, `Recent Official Visits`, `Leaves Availed`, `Leaves Remaining`, `Education Qualification`, `Institute`, `Type of Mobile Phone (Official)`, `Type of Mobile Phone (Personal)`) VALUES ('$data[0]', '$data[1]', '$data[2]', '$data[3]', '$data[4]', '$data[5]', '$data[6]', '$data[7]', '$data[8]', '$data[9]', '$data[10]', '$data[11]', '$data[12]', '$data[13]', '$data[14]', '$data[15]', '$data[16]', '$data[17]', '$data[18]')");
		
		//echo "INSERT INTO TABLE VALUES " . $data_field;
		echo "Inserted the data!!!";
		echo "<br>";
		
	}
	fclose($open);
	
}
else
{
	echo "File is not correct!!";
}

// 27.272727272727



?>