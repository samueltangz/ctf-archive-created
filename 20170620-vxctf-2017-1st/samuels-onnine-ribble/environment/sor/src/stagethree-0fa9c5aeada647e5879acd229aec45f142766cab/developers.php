<?php
    require("../functions.inc.php");
    display_header();
?>

            <div class=title>第 3 關</div><br>

            <p style="text-align:center">
                <img src="../images/questionmark.png" style="text-align:center;">
            </p>

            <form onsubmit="return submitAnswer();" style='text-align:center;'>
                <input type="text" id="answer">
                <input type="submit" value="輸入答案">
            </form>
            <script>
            var _0xbe19=["\x76\x61\x6C\x75\x65","\x61\x6E\x73\x77\x65\x72","\x67\x65\x74\x45\x6C\x65\x6D\x65\x6E\x74\x42\x79\x49\x64","\x73\x6E\x65\x61\x6B\x79\x73\x6E\x65\x61\x6B\x79","\x2E\x2E\x2F\x73\x74\x61\x67\x65\x66\x6F\x75\x72\x2D\x66\x39\x62\x32\x61\x35\x37\x35\x35\x31\x31\x39\x62\x36\x35\x66\x33\x64\x34\x61\x61\x32\x35\x37\x34\x62\x65\x39\x30\x30\x30\x63\x61\x65\x64\x30\x35\x38\x64\x38\x2F","\x2E\x70\x68\x70","\x72\x65\x70\x6C\x61\x63\x65","\x6C\x6F\x63\x61\x74\x69\x6F\x6E","\x57\x72\x6F\x6E\x67\x20\x41\x6E\x73\x77\x65\x72\x21\x21\x21"];function submitAnswer(){ answer= document[_0xbe19[2]](_0xbe19[1])[_0xbe19[0]];if(answer== _0xbe19[3]){window[_0xbe19[7]][_0xbe19[6]](_0xbe19[4]+ answer+ _0xbe19[5])}else {alert(_0xbe19[8])};return false }
            </script>
<?php
    display_footer();
?>