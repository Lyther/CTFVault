<?php

session_start();

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/utils.php';
require_once __DIR__ . '/auth.php';

$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    if (auth_login($username, $password, $error)) {
        header('Location: index.php');
        exit;
    }
}

?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Вход — <?= h(APP_NAME) ?></title>
    <style>
        :root {
            --accent: #4aa3ff;
            --accent2: #2f6bff;
            --ring: rgba(74, 163, 255, 0.35);
            --radius: 14px;
        }
        body {
            font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
            background:
                radial-gradient(900px 450px at 20% 0%, rgba(74, 163, 255, 0.35), transparent 60%),
                radial-gradient(800px 500px at 80% 10%, rgba(47, 107, 255, 0.25), transparent 55%),
                #071126;
            color: #e7efff;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .box {
            background: rgba(8, 18, 42, 0.78);
            padding: 2rem;
            border-radius: var(--radius);
            width: 320px;
            border: 1px solid rgba(231, 239, 255, 0.12);
            box-shadow: 0 18px 50px rgba(0,0,0,0.35);
        }
        h1 {
            margin-top: 0;
            margin-bottom: 1rem;
            font-size: 1.4rem;
            text-align: center;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 0.7rem 0.8rem;
            margin-bottom: 0.75rem;
            border-radius: 12px;
            border: 1px solid rgba(231, 239, 255, 0.12);
            background: rgba(255,255,255,0.06);
            color: #e7efff;
            outline: none;
        }
        input:focus {
            border-color: rgba(74,163,255,0.55);
            box-shadow: 0 0 0 4px var(--ring);
        }
        button {
            width: 100%;
            padding: 0.65rem 0.85rem;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            color: #fff;
            cursor: pointer;
            font-weight: 650;
        }
        button:hover { box-shadow: 0 0 0 4px var(--ring); }
        .error {
            margin-bottom: 0.75rem;
            padding: 0.5rem;
            border-radius: 12px;
            background: rgba(255, 90, 90, 0.18);
            border: 1px solid rgba(255, 90, 90, 0.35);
        }
        .links {
            margin-top: 0.75rem;
            font-size: 0.9rem;
            text-align: center;
            color: rgba(231, 239, 255, 0.75);
        }
        a {
            color: #9fd3ff;
            text-decoration: none;
        }
    </style>
</head>
<body>
<div class="box">
    <h1>Вход</h1>
    <?php if ($error): ?>
        <div class="error"><?= h($error) ?></div>
    <?php endif; ?>
    <form method="post">
        <label>
            Логин:
            <input type="text" name="username" required>
        </label>
        <label>
            Пароль:
            <input type="password" name="password" required>
        </label>
        <button type="submit">Войти</button>
    </form>
    <div class="links">
        Нет аккаунта? <a href="register.php">Регистрация</a><br>
        <a href="index.php">← На главную</a>
    </div>
</div>
</body>
</html>

