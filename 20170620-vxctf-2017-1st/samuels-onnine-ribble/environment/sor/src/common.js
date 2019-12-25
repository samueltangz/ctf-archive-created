function formA(action){
 if(action=="login"){
  $("#formMainA").html("<form method='POST' onsubmit='ajaxPost(this,1); return false;'><table><tr><td>帳號</td><td><input type='text' name='username'></td></tr><tr><td>密碼</td><td style='width:300px;'><input type='password' name='password'></td></tr><tr><td valign=top style='padding-top:6px;'>驗証碼　</td><td><input type='text' name='captcha'><br><img src='../../../../riddle/captcha.php?rand="+Math.random()+"' id='captcha' style='width:220px;height:70px;'></td></tr><tr><td colspan=3 style='text-align:center;'><input type='submit' value='登入'></td></tr><tr><td colspan=2><div id='messageDiv' style='display:none;'></td></tr></table><input type=hidden name=action value=login></form>");
  $("#tdLogin").addClass("selected");
  $("#tdRegister").removeClass("selected");
 } else if(action=="register"){
  $("#formMainA").html("<form method='POST' onsubmit='ajaxPost(this,1); return false;'><table><tr><td>帳號</td><td><input type='text' name='username'>（5 至 15 英數字元）</td></tr><tr><td>密碼</td><td style='width:300px;'><input type='password' name='password'></td></tr><tr><td>確認密碼</td><td><input type='password' name='password2'></td></tr><tr><td valign=top style='padding-top:6px;'>驗証碼</td><td><input type='text' name='captcha'><br><img src='../../../../riddle/captcha.php?rand="+Math.random()+"' id='captcha' style='width:220px;height:70px;'></td></tr><tr><td colspan=3 style='text-align:center;'><input type='submit' value='註冊'></td></tr><tr><td colspan=2><div id='messageDiv' style='display:none;'></td></tr></table><input type=hidden name=action value=register></form>");
  $("#tdRegister").addClass("selected");
  $("#tdLogin").removeClass("selected");
 }
}

function ajaxPost(form,ifSerial){
 if(ifSerial){ form=$(form).serialize(); }

 $.ajax({
  type: "POST",
  url: "../../../../riddle/ajaxpost.php",
  data: form
 }).done(function(msg){
  eval(msg);
 });
}






function blink(){
 $("body").css("background-color","#000000");
 setTimeout('$("body").css("background-color","#ffffff");',50);
 setTimeout('blink();',Math.random()*4500+500);
}