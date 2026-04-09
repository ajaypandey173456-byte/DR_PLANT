<?php
$conn = new mysqli("localhost", "root", "", "user_system");

// Handle CREATE
if (isset($_POST['add'])) {
    $u = $_POST['username'];
    $e = $_POST['email'];
    $conn->query("INSERT INTO users (username, email) VALUES ('$u', '$e')");
}

// Handle DELETE
if (isset($_GET['delete'])) {
    $id = $_GET['delete'];
    $conn->query("DELETE FROM users WHERE id=$id");
}

// Handle READ
$users = $conn->query("SELECT * FROM users");
?>

<!DOCTYPE html>
<html>
<body>
    <h2>User Management (CRUD)</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="email" name="email" placeholder="Email" required>
        <button type="submit" name="add">Add User</button>
    </form>

    <table border="1" style="margin-top:20px; width:50%;">
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Action</th></tr>
        <?php while($row = $users->fetch_assoc()): ?>
        <tr>
            <td><?= $row['id'] ?></td>
            <td><?= $row['username'] ?></td>
            <td><?= $row['email'] ?></td>
            <td><a href="?delete=<?= $row['id'] ?>">Delete</a></td>
        </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>