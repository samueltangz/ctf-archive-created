<?php
    require("functions.inc.php");
    $login_warning = NULL;
    if(isset($_POST['username']) && isset($_POST['password'])){
        $login_warning = 0;
        $username = $_POST['username'];
        $password = $_POST['password'];
        if(validate_username($username) == true && validate_password($password) == true){
            $result = $mysqli->query("SELECT `uid` FROM `users` WHERE `username` = '{$username}' AND `password` = SHA2('{$password}', 256)");
            if($result->num_rows == 1){
                $row = $result->fetch_row();
                $cookie_value = str_pad((int)$row[0], 10, '0', STR_PAD_LEFT) . substr(hash('sha256', $password), 0, 10);
                setcookie('esblog', $cookie_value); 
            } else {
                $login_warning = 2;
            }
        } else {
            $login_warning = 1;
        }
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Enormous Little Blog - Login</title>
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href="css/common.css" rel="stylesheet">
    </head>

    <body>
        <div class="blog-masthead">
            <div class="container">
                <nav class="blog-nav">
                    <a class="blog-nav-item" href=".">Home</a>
                    <a class="blog-nav-item active" href="login.php">Login</a>
                </nav>
            </div>
        </div>

        <div class="container">

            <div class="blog-header">
                <h1 class="blog-title">Enormous Little Blog</h1>
                <p class="lead blog-description">Compiled by Team Don Enormous, a group of professional hackers.</p>
            </div>

            <div class="row">
                <div class="col-sm-12 blog-main">

<?php
    if(isset($login_warning)){
        if($login_warning == 0){
?>

                    <div class="alert alert-success">
                        <strong>Success!</strong> Logined successfully.
                    </div>

<?php
        } elseif($login_warning == 1){
?>

                    <div class="alert alert-danger">
                        <strong>Error!</strong> Your username or password is not composed of alphanumeric letters between 5 and 12 characters.
                    </div>

<?php
        }  elseif($login_warning == 2){
?>

                    <div class="alert alert-danger">
                        <strong>Error!</strong> Your username / password is incorrect.
                    </div>

<?php
        } 
    }
?>



                    <div class="col-sm-4 col-md-offset-4">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title">Please sign in</h3>
                            </div>
                            <div class="panel-body">
                                <form method=POST role="form">
                                <fieldset>
                                    <div class="form-group">
                                        <input class="form-control" placeholder="Username" name="username" type="text">
                                    </div>
                                    <div class="form-group">
                                        <input class="form-control" placeholder="Password" name="password" type="password" value="">
                                    </div>
                                    <input class="btn btn-md btn-success btn-block" type="submit" value="Login">
                                    <input class="btn btn-md btn-warning btn-block" type="button" value="Register" onclick="alert('Register is closed. Please find the administrator to create an account.');">
                                </fieldset>
                                </form>
                            </div>
                        </div>
                    </div>


                </div><!-- /.blog-sidebar -->
            </div><!-- /.row -->
        </div><!-- /.container -->

        <footer class="blog-footer">
            <p>Blog template built for <a href="http://getbootstrap.com">Bootstrap</a> by <a href="https://twitter.com/mdo">@mdo</a>. Blog template used by <em>Team Don Enormous</em>, which is just a virtual team created for WEB250 challenge in VXCTF.</p>
            <p>
                <a href="#">Back to top</a>
            </p>
        </footer>
        <script src="js/jquery-3.2.1.min.js"></script>
        <script src="js/bootstrap.min.js"></script>
    </body>
</html>
