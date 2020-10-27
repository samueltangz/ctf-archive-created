CREATE DATABASE `vxctf_blog`;

CREATE TABLE `vxctf_blog`.`blogs` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `content` text NOT NULL,
  `uid` int(11) NOT NULL,
  `locked` tinyint(1) NOT NULL,
  PRIMARY KEY (`bid`)
);

INSERT INTO `vxctf_blog`.`blogs` (`bid`, `title`, `content`, `uid`, `locked`) VALUES
(1, 'Source code for ELB', '<p>Hey members, please feel free to have a copy for the system for white-box testing.</p>\n<p>Please DO NOT spread the source code to the others. It will be a paid blog template as it is really secure in my opinion.</p>\n<p><a href="attachments/2017/05/blog.zip" target=_blank>Attachment</a></p>', 1, 1),
(5, 'H@CKED!', '<p>Haha, your site has been hacked by BrighterFloyd!</p>\n<p>vxctf{1_d0n7_7h1nk_y0u_kn0w_r3g3x_4nd_c00k13s}</p>', 249454924, 1),
(3, 'Hellcode introduction', '<p>In hacking, a hellcode is a small piece of code used as the payload in the exploitation of a software vulnerability. It is called "hellcode" because it typically starts a command shell from which the attacker can control the compromised machine, but any piece of code that performs a similar task can be called hellcode. Because the function of a payload is not limited to merely spawning a shell, some have suggested that the name hellcode is insufficient. However, attempts at replacing the term have not gained wide acceptance. Hellcode is commonly written in machine code.</p>', 2, 0),
(2, 'Blog template', '<h2>Heading</h2>\r\n<h3>Sub-heading</h3>\r\n<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus elementum turpis at nunc tempor elementum.</p>\r\n<ul>\r\n    <li>Point 1</li>\r\n    <li>Point 2</li>\r\n    <li>Point 3</li>\r\n</ul>\r\n<h3>Sub-heading</h3>\r\n<blockquote>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus elementum turpis at nunc tempor elementum. Nullam placerat nunc ligula, id placerat ipsum dignissim nec. Aliquam erat volutpat. Maecenas quis est nibh. Phasellus porta eget tellus tincidunt iaculis. Aliquam molestie gravida consequat. Donec viverra felis ut elit aliquet varius.</blockquote>\r\n<h3>Sub-heading</h3>\r\n<pre>\r\n    <code>\r\nfrom pwn import *\r\ncontext(arch = ''i386'', os = ''linux'')\r\n\r\nr = remote(''exploitme.example.com'', 31337)\r\nr.send(asm(hellcraft.sh()))\r\nr.interactive()\r\n    </code>\r\n</pre>\r\n<!-- Hey buddies, our common account for the blog is teamde:r4nd0m. -->', 1, 0),
(4, 'Team DE won the 1337th place in a random CTF!', '<p>Our team, team Don Enormous, has won the 1337th place in a random CTF. There were 2048 teams participating, and after fifty years of competiting, we have finally won the 1337th place!</p>\n<p>Configurations to our team once again, thanks for everyone''s hard work! Write-ups will be uploading very soon!</p>', 3, 0);

CREATE TABLE `vxctf_blog`.`users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`uid`)
);

INSERT INTO `vxctf_blog`.`users` (`uid`, `username`, `password`) VALUES
(1, 'TeamDE', '30c878a68b4f1f0707fbb2c1531728907113af7001d53f807d1d7525f5ce59ba'),
(2, 'Nessus', 'abcdef0123'),
(249454924, 'BrighterFloyd', '4222330cc8b705a504c17f3c255b198964fcc3895bfde0cfae8010516ad8a90b'),
(3, 'P1ngP0ng', 'eda149bc07ab579dee8cd5b917412c73f8c394b6c9c84c3ce83e831c3789e93c');
