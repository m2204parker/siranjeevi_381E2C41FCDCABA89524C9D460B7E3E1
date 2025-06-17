<?php
$n = $_POST['uname'];
$c = $_POST['mail'];
$d = $_POST['password'];

// Establish database connection
$con = mysqli_connect("localhost", "root", "", "signin");

// Check connection
if (!$con) {
    die("Connection failed: " . mysqli_connect_error());
}

// Prevent SQL injection
$n = mysqli_real_escape_string($con, $n);
$c = mysqli_real_escape_string($con, $c);
$d = mysqli_real_escape_string($con, $d);

// SQL query
$sql = "INSERT INTO users (userename, emailid, password) VALUES ('$n', '$c', '$d')";

// Execute query
$r = mysqli_query($con, $sql);

if ($r) {
    echo "Sign in successfully";
} else {
    echo "Data can't be added: " . mysqli_error($con);
}

// Close connection
mysqli_close($con);
?>
