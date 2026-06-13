<?php

require_once __DIR__ . '/config.php';

class Logger
{
    public $logFile;
    public $message;

    public function __construct(string $file = null)
    {
        $this->logFile = $file ?? DATA_DIR . '/app.log';
        $this->message = '';
    }

    public function __destruct()
    {
        if (!is_string($this->logFile)) {
            return;
        }
        $msg = (string)($this->message ?? '');
        if ($msg === '') {
            return;
        }
        @file_put_contents($this->logFile, $msg . PHP_EOL, FILE_APPEND);
    }
}

class FileHandler
{
    public $path;
    public $mode = 'r';

    public function __wakeup()
    {
        if (!is_string($this->path)) {
            return;
        }
        $h = @fopen($this->path, $this->mode);
        if ($h) {
            @fclose($h);
        }
    }
}

class Cache
{
    public $data = [];

    public function __toString()
    {
        return json_encode($this->data, JSON_UNESCAPED_UNICODE);
    }
}

class User
{
    public $username;
    public $role = 'guest';
}

