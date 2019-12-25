<?php
    require("../functions.inc.php");
    display_header();
?>

            <div class=title>第 1 關</div><br>

            <p style="text-align:center">
                <img src="../images/questionmark.png" style="text-align:center;">
            </p>

            <form onsubmit="return submitAnswer();" style='text-align:center;'>
                <input type="text" id="answer">
                <input type="submit" value="輸入答案">
            </form>
            <script>
            function submitAnswer(){
                answer = document.getElementById('answer').value;
                if(answer == 'exclamationmark'){
                    window.location.replace("../stagetwo-77ff586c21edaea97e2d1a95fd1b62074b7a16cb/" + answer + ".php");
                } else {
                    alert("Wrong Answer!!!");
                }
                return false;
            }
            </script>
<?php
    display_footer();
?>