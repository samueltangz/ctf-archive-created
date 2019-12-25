<?php
    require("../functions.inc.php");
    display_header();
?>

            <div class=title>第 4 關</div><br>

            <p style="text-align:center">
                <img src="../images/questionmark.png" style="text-align:center;">
            </p>

            <form onsubmit="return submitAnswer();" style='text-align:center;'>
                <input type="text" id="answer">
                <input type="submit" value="輸入答案">
            </form>
            <script>
            eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('9 a(){2=b.c(\'2\').8;3=1;6(i=0;i<2.4;i++){3*=2.7(i)}5(3==e){k.m.n("../p-l/"+2+".f")}h{j("q g!!!")}o d}',27,27,'||answer|checksum|length|if|for|charCodeAt|value|function|submitAnswer|document|getElementById|false|206847083506555800000|php|Answer|else||alert|window|5880bb3cc95edcf2c43e70ad4b1bdf895cdc62bd|location|replace|return|stagefive|Wrong'.split('|'),0,{}))
            </script>
<?php
    display_footer();
?>