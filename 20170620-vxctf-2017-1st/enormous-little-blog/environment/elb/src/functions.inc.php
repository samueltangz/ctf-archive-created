<?php
    $mysqli = new mysqli('db', 'root', 'dd7929a29b7140d1255f1610fd3ae2e7', 'vxctf_blog');
    if($mysqli->connect_error){
        die("Database connection failed: ". $mysqli->connect_error);
    }
    if(isset($_COOKIE['esblog'])){
        $esblog = $_COOKIE['esblog'];
    }
    $current_uid = NULL;
    $current_name = NULL;
    if(isset($esblog)){
        if(preg_match('/([0-9]{10})([0-9a-f]{10})/', $esblog, $matches) != 0){
            $uid = (int) $matches[1];
            $password = $matches[2];
            $result = $mysqli->query("SELECT `username` FROM `users` WHERE `uid` = {$uid} AND substr(`password`, 1, 10) = '{$password}'");
            if($result->num_rows == 1){
                $row = $result->fetch_row();
                $current_uid = $uid;
                $current_name = $row[0];
            }
        }
        if($current_uid == NULL){
            setcookie('esblog', NULL, time() + 1); 
            unset($esblog);
        }
    }

    function validate_username($username){
        if(strlen($username) < 5 || strlen($username) > 12){
            return false;
        }
        $username_array = str_split($username);
        foreach($username_array as $username_char){
            $username_char = ord($username_char);
            if($username_char >= ord('0') && $username_char <= ord('9')){
                continue;
            } elseif($username_char >= ord('a') && $username_char <= ord('z')){
                continue;
            } elseif($username_char >= ord('A') && $username_char <= ord('Z')){
                continue;
            }
            return false;
        }
        return true;
    }

    function validate_password($password){
        if(preg_match('/([0-9a-zA-Z]{5,12})/', $password, $matches2) == 1){
            return true;
        } else {
            return false;
        }
    }

?>