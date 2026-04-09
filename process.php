<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 1. Sanitize inputs to prevent Cross-Site Scripting (XSS)
    $username = htmlspecialchars(trim($_POST['username']));
    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL);
    $password = $_POST['password'];

    // 2. Simple Validation
    if (empty($username) || empty($email) || empty($password)) {
        die("Please fill all fields.");
    }

    // 3. Securely hash the password (Industry Standard)
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // 4. Output results (In a real app, you would save these to MySQL)
    echo "<h1>Registration Successful!</h1>";
    echo "Welcome, " . $username . "<br>";
    echo "Your password has been securely hashed as: " . $hashed_password;
} else {
    header("Location: register.html");
}
?>