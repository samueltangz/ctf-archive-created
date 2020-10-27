<?php
    require("functions.inc.php");

    $result = $mysqli->query("SELECT `bid`, `title`, `content`, `uid`, (SELECT `username` FROM `users` WHERE `users`.`uid` = `blogs`.`uid`), `locked` FROM `blogs` ORDER BY `bid` DESC");
    $blog_entries = array();
    while($row = $result->fetch_row()){
        $blog_entries[] = $row;
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Enormous Little Blog</title>
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href="css/common.css" rel="stylesheet">
    </head>

    <body>
        <div class="blog-masthead">
            <div class="container">
                <nav class="blog-nav">
                    <a class="blog-nav-item active" href=".">Home</a>

<?php if(isset($esblog)){ ?>

                    <a class="blog-nav-item" href="logout.php">Logout</a>

<?php } else { ?>

                    <a class="blog-nav-item" href="login.php">Login</a>

<?php } ?>

                </nav>
            </div>
        </div>

        <div class="container">

            <div class="blog-header">
                <h1 class="blog-title">Enormous Little Blog</h1>
                <p class="lead blog-description">Compiled by Team Don Enormous, a group of professional hackers.</p>
            </div>

            <div class="row">

                <div class="col-sm-8 blog-main">

<?php
    foreach($blog_entries as $blog_entry){
?>

                    <div class="blog-post" id="blog-<?php echo $blog_entry[0]; ?>">
                        <h2 class="blog-post-title"><?php echo $blog_entry[1]; ?></h2>
                        <p class="blog-post-meta">Written by <?php echo $blog_entry[4]; ?></p>

                        <?php
                            if($blog_entry[5] == 0 || $current_uid == $blog_entry[3]){
                                if($blog_entry[5] == 1){
                                    echo "<p><em>This blog entry is locked. One you could view this.</em></p>";
                                }
                                echo $blog_entry[2];
                            } else {
                                echo "<p><em>This blog entry is locked. Only {$blog_entry[4]} can view this.</em></p>";
                            }
                        ?>

                    </div><!-- /.blog-post -->

<?php } ?>

                </div><!-- /.blog-main -->

                <div class="col-sm-3 col-sm-offset-1 blog-sidebar">

<?php
    if(isset($esblog) && isset($current_name)){
?>

                    <div class="sidebar-module sidebar-module-inset">
                        <h4>Member's Zone</h4>
                        <p>Welcome back, <em><?php echo $current_name; ?></em>.</p>
                        <ul>
                            <li><a href="#" onclick="alert('To create a new post, please send an e-mail to the address allocated to you. It will be processed within 15 days.');">New Post</a></li>
                            <li><a href="logout.php">Logout</a></li>
                        </ul>
                    </div>

<?php
    } else {
?>

                    <div class="sidebar-module sidebar-module-inset">
                        <h4>Member's Zone</h4>
                        <p>Hi guest, if you are a member of Team Don Enormous, please login.</p>
                    </div>

<?php
    }
?>

                    <div class="sidebar-module sidebar-module-inset">
                        <h4>About</h4>
                        <p>Sincerely presented by <em>Team Don Enormous</em>. Each member are holder of CRISPY, PIZZA, CREAM. All are guaranteeded to weight 400 pounds.</p>
                    </div>
                    <div class="sidebar-module">
                        <h4>Recent Posts</h4>
                        <ol class="list-unstyled">

<?php
    foreach($blog_entries as $blog_entry){
?>

                            <li><a href="#blog-<?php echo $blog_entry[0]; ?>"><?php echo $blog_entry[1]; ?></a></li>

<?php
    }
?>

                        </ol>
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
