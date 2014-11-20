from django.contrib.sites.models import Site

__author__ = 'orion'

try:
    current_site = Site.objects.get_current()
except:
    current_site = 'migration'
def get_auto_refresh_code(mirror_code, current_level):
    auto_refresh_url = "http://%s/auto_up/%s/%s/" % (current_site.domain, mirror_code, current_level)

    auto_refresh_code = """
    <script type="text/javascript">
   //     {#        var st = $("a",".levelstats").attr("href");#}
     //   {#        var c_level = st.substr(st.search("level=[0-9]+")+6,st.indexOf("&")-st.search("level=[0-9]+")-6);#}
        var c_level = "%s";
        var URL = "%s";
        function autorefresh() {
            $.ajax({
                url: URL,
                success: function (data) {
                    if (data != c_level) {
                        document.location.href = document.location.href;

                    } else {
                        autorefresh();
                    }
                },
                error: function (e,e1,e2) {
                    if(e2=='NOT FOUND'){
                    console.log('404 stop autorefresh');
                    return 1;
                    }else{
                    setTimeout(function(){autorefresh();},2000);
                    }
                }
            })
        }
        $(document).ready(function () {
            autorefresh();
        });

    </script>

"""%(current_level,auto_refresh_url)
    return auto_refresh_code