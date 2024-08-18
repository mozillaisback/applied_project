<?php

$conn = new mysqli(db:port,"username","password","defaultdb");
$result = $conn->query("select distinct `categories` from categories_for_prompt");

echo "<html>";
echo "<body>";
echo '<form method="post" action="process.php">';
echo "<legend><strong>Select the Data !!!! </strong></legend>";
echo "<br>";
echo "<br>";

echo "<p style='color: blue;'>Select the category from below</p>";
echo "<select name='categories'>";
while ($row = $result->fetch_assoc()) {
  $categories = $row['categories'];
  echo '<option value="'.htmlspecialchars($categories).'">'.htmlspecialchars($categories).'</option>';
}


echo "</select>";

echo "<br>";

echo "<br>";

$result = $conn->query("select distinct `sub_categories` from categories_for_prompt");
echo "<p style='color: blue;'>Select the sub category from below</p>";
echo "<select name='sub_categories'>";
while ($row = $result->fetch_assoc()) {
  $sub_categories = $row['sub_categories']; 
  echo '<option value="'.htmlspecialchars($sub_categories).'">'.htmlspecialchars($sub_categories).'</option>';
}
echo "</select>";

echo "<br>";

echo "<br>";



//echo "<p style='color: blue;'>Enter the prompt below </p>";
//echo '	<input type="text" name="comment">';
echo '	<input type="submit" name="submit" value="Submit">';
echo '</form>';


echo "</body>";
echo "</html>";



?>


