<?php
    require("../functions.inc.php");
    display_header();
?>

            <div class=title>第 2 關</div><br>

            <p style="text-align:center">
                <img src="../images/questionmark.png" style="text-align:center;">
            </p>

            <form onsubmit="return submitAnswer();" style='text-align:center;'>
                <input type="text" id="answer">
                <input type="submit" value="輸入答案">
            </form>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/sha1.js"></script>
            <script>
            function submitAnswer(){
                answer = document.getElementById('answer').value;
                if(CryptoJS.SHA1(answer) == '96454d3f93dcac9bc142e6891206709671e77725'){
                    window.location.replace("../stagethree-0fa9c5aeada647e5879acd229aec45f142766cab/" + answer + ".php");
                } else {
                    alert("Wrong Answer!!!");
                }
                return false;
            }
            </script>
<?php
    display_footer();
?>