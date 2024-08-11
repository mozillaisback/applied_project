<?php

declare(strict_types=1);

// redirect to upload form if no file has been uploaded or an error occurred
if (!isset($_FILES['fileToUpload']) || $_FILES['fileToUpload']['error'] > 0) {
  header('Location: index.html');
  exit;
}

// configuration
$uploadDirectory = getcwd() . '/uploads/';
$fileExtensionsAllowed = ['xlsx', 'csv', 'txt']; // These will be the only file extensions allowed
$mimeTypesAllowed = ['text/plain', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']; // These will be the only mime types allowed
$maxFileSizeInBytes = 1024 * 1024 * 5; // 5 megabytes

// extract data about the uploaded file
['name' => $fileName, 'tmp_name' => $fileTempName, 'type' => $fileType, 'size' => $fileSize] = $_FILES['fileToUpload'];
['extension' => $fileExtension] = pathinfo($fileName);

$errors = [];

// validate the file extension is in our allow list
if (!in_array($fileExtension, $fileExtensionsAllowed, strict: true)) {
  $errors[] = 'File must have one of the following extensions: ' . implode(', ', $fileExtensionsAllowed) . '.';
}

// validate the file is an allowed mime type based on actual contents
$detectedType = mime_content_type($fileTempName) ?: 'unknown type';
if (!in_array($detectedType, $mimeTypesAllowed, strict: true)) {
  $errors[] = 'File must have one of the following mime types: ' . implode(', ', $mimeTypesAllowed) . '.';
}

// validate if the file already exists
$uploadPath = $uploadDirectory . $fileName;
if (file_exists($uploadPath)) {
  $errors[] = 'File with the same name already exists.';
}

// validate the maximum file size
if ($fileSize > $maxFileSizeInBytes) {
  $errors[] = 'File must not be greater than ' . number_format($maxFileSizeInBytes) . ' bytes.';
}

// verify for errors and move the file upon successful validation
if (count($errors) > 0) {
  echo '<h3>Errors</h3>';
  echo '<ul>';
  foreach ($errors as $error) {
    echo '<li>' . $error . '</li>';
  }
  echo '</ul>';

  exit;
}

if (move_uploaded_file($fileTempName, $uploadPath)) {
  echo 'The file has been successfully uploaded.';
  echo $fileName;
  echo "<br>";
  include 'php_sql.php';
} else {
  echo 'There was an error uploading your file.';
}