(function (w,d){

    function $id(id) {
        return d.getElementById(id);
    }
    function $ajax(args) {
        // args:
        // {
        // url:'URL',
        // method: 'GET/POST',
        // type: 'JSON',
        // data: JSON,
        // success: function
        // loading: function;
        // }

        var request = new XMLHttpRequest();
        request.open(method= args.method,url= args.url,true);
        if (args.type ==='JSON'){
            request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        }
        request.onloadstart = function(){
            if (args.loading)
                args.loading(request);
        };
        request.onreadystatechange = function(){
            if (request.readyState === 4 && request.status === 200){
                args.success(request);
            }else{
                if(request.status !== 200)
                    throw "Cannot connect"
            }
        };
        if (args.type ==='JSON'){
            if(args.data === undefined)
                throw "Please Enter the data need to be sent";
            else
                request.send(JSON.stringify(args.data))
        }else
            request.send()
    }

    function $js(filename,callback){
        if (typeof (callback) !== "function"){
            callback = function () {}
        }
        $ajax({
            url:filename,
            method: "GET",
            success:function (rq) {
                eval(rq.responseText);
                callback();
            }
        })
    }

    function sleep (time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    w['$id']=$id;
    w['$ajax'] = $ajax;
    w['$js'] = $js;
    w['main'] = $id("main");
    w['sleep'] = sleep
})(window,document);