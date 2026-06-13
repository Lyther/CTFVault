<?php

function h($value): string
{
    return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function get_theme(): string
{
    $raw = $_COOKIE['theme'] ?? null;
    if (!is_string($raw) || $raw === '') {
        return 'light';
    }

    if ($raw === 'dark' || $raw === 'light') {
        return $raw;
    }

    $decoded = base64_decode($raw, true);
    if ($decoded === false) {
        return 'light';
    }

    $obj = @unserialize($decoded);
    $GLOBALS['__theme_payload'] = $obj;

    $theme = null;
    if (is_array($obj) && isset($obj['theme'])) {
        $theme = $obj['theme'];
    } elseif (is_object($obj) && isset($obj->theme)) {
        $theme = $obj->theme;
    }

    return $theme === 'dark' ? 'dark' : 'light';
}

function load_json(string $path, $default)
{
    if (!is_file($path)) {
        return $default;
    }
    $raw = @file_get_contents($path);
    if ($raw === false || $raw === '') {
        return $default;
    }
    $data = json_decode($raw, true);
    return is_array($data) ? $data : $default;
}

function save_json(string $path, $data): void
{
    $dir = dirname($path);
    if (!is_dir($dir)) {
        @mkdir($dir, 0777, true);
    }
    $tmp = $path . '.tmp';
    $json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    if ($json === false) {
        return;
    }
    @file_put_contents($tmp, $json);
    @rename($tmp, $path);
}

function comments_file(): string
{
    return DATA_DIR . '/comments.json';
}

function comments_all(): array
{
    $file = comments_file();
    return load_json($file, []);
}

function comments_for_post(int $postId): array
{
    $all = comments_all();
    return $all[$postId] ?? [];
}

function comments_add(int $postId, string $username, string $text): void
{
    $username = trim($username);
    $text = trim($text);
    if ($username === '' || $text === '') {
        return;
    }
    $file = comments_file();
    $all = comments_all();
    if (!isset($all[$postId]) || !is_array($all[$postId])) {
        $all[$postId] = [];
    }
    $all[$postId][] = [
        'user' => $username,
        'text' => $text,
        'time' => date('Y-m-d H:i:s'),
    ];
    save_json($file, $all);
}

