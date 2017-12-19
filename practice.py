content = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=9" />
    <meta http-equiv="imagetoolbar" content="no" />
    <title>Get custom output  204001 rscf_org Download Custom 00:00_20/12/2012-00:00_20/12/2017</title>
        <style type="text/css">body { overflow:hidden; }</style>
    <base href="http://realtimedata.water.nsw.gov.au/" target="_self" />
    <link rel="stylesheet" type="text/css" href="wsys/webhyd.wsys.css?20171220064728" />
    <link rel="stylesheet" type="text/css" href="wini/webhyd.wini.css?20171220064728" />
    <script type="text/javascript">var webhydcss_old = false;</script>
    
    <script type="text/javascript" src="wsys/jquery.2.2.4.min.js"></script>
    <script type="text/javascript" src="wsys/websniffer.js?20171220064728"></script>
    <script type="text/javascript" src="wsys/webhyd.min.js?20171220064728"></script>
        <script type="text/javascript">
      var cfg_coreframes = new Array('menu','intro','help','admin','ws');

      Cookies.create('username',"webuser");
      Cookies.create('userid',"818542479");
      Cookies.create('userclass',"anon");
      Cookies.create('is_admin',"0");
      console.log('init_app 2 is_admin:0 window['+window.name+']');
      Cookies.create('language','English');
    </script>
    
  </head>
<script  type="text/javascript">console.log('running WebHyd::get_custom_output()');</script>
  <body onload="onLoad()" class="output">
    <script type="text/javascript" src="wsys/jquery.floatThead.2.0.0.min.js"></script>
    <div id="wrapper">
      <span id="datatabletop">
        <button class="float_button" onclick="goback()">Go back</button> &nbsp; <span id="msg"></span>
        <br /><br />
      </span>
<script type="text/javascript">
  msgbox('Please wait while data is prepared for the zip file download');
  function onLoad() {
    hide_object('msgbox',webhyd_frame.document);
    fixallimages();
    document.getElementById('wrapper').style.fontSize = menuloc.fontadj;
    $('table.block').floatThead();
    var windowheight       = $(window).height();
    var datatabletopheight = $('#datatabletop').height();
    var titleheight        = $('#datatabletitle').height();
    var abovedataheight    = $('#abovedata').height();
    var footerheight       = $('#datatablefooter').height();
    var pagefooterheight   = $('#pagefooter').height();
    var tableheight        = windowheight - datatabletopheight - titleheight - abovedataheight - footerheight - pagefooterheight - 40;
    $('.scrollcontainer').height( tableheight );
    console.log('windowheight ['+windowheight+']\ndatatabletopheight ['+datatabletopheight+']\ntitleheight ['+titleheight+']\nabovedataheight ['+abovedataheight+']\nfooterheight ['+footerheight+']\npagefooterheight ['+pagefooterheight+']\ntableheight ['+tableheight+']');

    // give the window the focus so that keystrokes can be captured; ESC will replicate the Go Back button
    window.focus();
    document.body.onkeyup = function (e) {
      e = e || window.event;
      var keystroke = e.keyCode || e.which;
      console.log('_key_up keystroke ['+keystroke+'] output frame');
      if (keystroke == 27) goback();
    }
  }
  function goback() {
    menuloc.display_frame(menuloc.catid,'rscf_org');
    $('.scrollcontainer').scrollTop(0);
  }
</script></thead>
<tbody>
</table>
</div>
<br />.. more than 2000 lines returned<br /><span class="anchor" onclick="location.href='http://realtimedata.water.nsw.gov.au/wgen/users//818542479/204001_20171220.zip?20171220064728';">click here to download 15 minutes data zip file</span><br />
<div id="zipdiv" style="display:none">
7-Zip (A) 2.30 Beta 32  Copyright (c) 1999-2003 Igor Pavlov  2003-05-15
Scanning

Creating archive 204001_20171220.zip

Compressing  204001.csv

Everything is Ok
</div><script type="text/javascript">
  parent.rsrscf_org.document.getElementById('download').innerHTML='<span class="anchor" onclick="location.href=\'http://realtimedata.water.nsw.gov.au/wgen/users//818542479/204001_20171220.zip?20171220064728\';" id="downloadlink">click here to download 15 minutes data zip file</span>';
  parent.rsrscf_org.document.getElementById('download').style.display = 'block';
</script>
  </div>
  <span id="pagefooter"></span>
</body>
</html>'''

print('downloadlink' in content)
for row in content.split('\n'):
    if 'downloadlink' in row:
        print(row)
        link_url = row.split('onclick="location.href=\'')[1]
        link_url = link_url.split('\';" id="downloadlink">')[0]
        # link_url = link_url[:len(link_url)-78]
        print(link_url)