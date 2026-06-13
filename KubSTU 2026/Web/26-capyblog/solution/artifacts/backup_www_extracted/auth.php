<?php

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/utils.php';

const USERS_FILE = DATA_DIR . '/users.json';

function auth_load_users(): array
{
    $file = USERS_FILE;
    $data = load_json($file, []);
    return is_array($data) ? $data : [];
}

function auth_save_users(array $users): void
{
    save_json(USERS_FILE, $users);
}

function auth_current_user(): ?string
{
    return isset($_SESSION['user']) && is_string($_SESSION['user'])
        ? $_SESSION['user']
        : null;
}

function auth_is_logged_in(): bool
{
    return auth_current_user() !== null;
}

function auth_register(string $username, string $password, ?string &$error = null): bool
{
    $username = trim($username);
    if ($username === '' || $password === '') {
        $error = 'Имя пользователя и пароль не могут быть пустыми.';
        return false;
    }
    if (!preg_match('/^[a-zA-Z0-9_]{3,20}$/u', $username)) {
        $error = 'Имя может содержать только латинские буквы, цифры и _. Длина 3–20 символов.';
        return false;
    }

    $users = auth_load_users();
    if (isset($users[$username])) {
        $error = 'Такой пользователь уже существует.';
        return false;
    }

    $users[$username] = [
        'password' => password_hash($password, PASSWORD_DEFAULT),
        'created_at' => date('Y-m-d H:i:s'),
    ];
    auth_save_users($users);

    $_SESSION['user'] = $username;
    return true;
}

function auth_login(string $username, string $password, ?string &$error = null): bool
{
    $username = trim($username);
    $users = auth_load_users();
    if (!isset($users[$username])) {
        $error = 'Неверные логин или пароль.';
        return false;
    }
    $hash = $users[$username]['password'] ?? '';
    if (!is_string($hash) || !password_verify($password, $hash)) {
        $error = 'Неверные логин или пароль.';
        return false;
    }
    $_SESSION['user'] = $username;
    return true;
}

function auth_logout(): void
{
    unset($_SESSION['user']);
}

