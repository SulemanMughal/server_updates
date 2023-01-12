$(function(){
    $("form#login_form").on("submit",function(event){
      event.preventDefault();
      event.stopPropagation();
      var submit_form = $("form#login_form").get(0);
      var btn = $("#login_submit_btn");
      if(submit_form.checkValidity()){
        // $(btn).buttonLoader('start');
        var fd = new FormData($("form#login_form")[0]);
        $.ajaxSetup({
          beforeSend: function(xhr, settings){
            xhr.setRequestHeader(
              'X-CSRFToken', '{{ csrf_token }}'
            )
          }
        });
        $.ajax({
          url : $(submit_form).attr("action"),
          type  : "POST",
          data: fd,
          processData: false,
          contentType: false,
          success : function(response){
            new Noty({
              //  alert, success, error, warning, info
              timeout: 5000,
              type : "success",
              theme: 'sunset',
              // container : ".noty_layout",
              force : false,
              // layout: 'bottomLeft',
            //   text: 'Logged in successfully',
              text: response["message"],
              animation: {
  open: function (promise) {
      var n = this;
      var Timeline = new mojs.Timeline();
      var body = new mojs.Html({
          el        : n.barDom,
          x         : {500: 0, delay: 0, duration: 500, easing: 'elastic.out'},
          isForce3d : true,
          onComplete: function () {
              promise(function(resolve) {
                  resolve();
              })
          }
      });

      var parent = new mojs.Shape({
          parent: n.barDom,
          width      : 200,
          height     : n.barDom.getBoundingClientRect().height,
          radius     : 0,
          x          : {[150]: -150},
          duration   : 1.2 * 500,
          isShowStart: true
      });

      n.barDom.style['overflow'] = 'visible';
      parent.el.style['overflow'] = 'hidden';

      var burst = new mojs.Burst({
          parent  : parent.el,
          count   : 10,
          top     : n.barDom.getBoundingClientRect().height + 75,
          degree  : 90,
          radius  : 75,
          angle   : {[-90]: 40},
          children: {
              fill     : '#EBD761',
              delay    : 'stagger(500, -50)',
              radius   : 'rand(8, 25)',
              direction: -1,
              isSwirl  : true
          }
      });

      var fadeBurst = new mojs.Burst({
          parent  : parent.el,
          count   : 2,
          degree  : 0,
          angle   : 75,
          radius  : {0: 100},
          top     : '90%',
          children: {
              fill     : '#EBD761',
              pathScale: [.65, 1],
              radius   : 'rand(12, 15)',
              direction: [-1, 1],
              delay    : .8 * 500,
              isSwirl  : true
          }
      });

      Timeline.add(body, burst, fadeBurst, parent);
      Timeline.play();
  },
  close: function (promise) {
      var n = this;
      new mojs.Html({
          el        : n.barDom,
          x         : {0: 500, delay: 10, duration: 500, easing: 'cubic.out'},
          skewY     : {0: 10, delay: 10, duration: 500, easing: 'cubic.out'},
          isForce3d : true,
          onComplete: function () {
              promise(function(resolve) {
                  resolve();
              })
          }
      }).play();
  }
}
      }).show(); 
                  setTimeout(function(){
                    window.location.href=response["next_url"];
                  }, 1000);
                  
                //   $(btn).buttonLoader('stop');
          },
          error : function(response){
            new Noty({
              //  alert, success, error, warning, info
              timeout: 5000,
              type : "error",
              theme: 'sunset',
              // container : ".noty_layout",
              force : false,
              // layout: 'bottomLeft',
              text: response["responseJSON"]["error"],
              animation: {
  open: function (promise) {
      var n = this;
      var Timeline = new mojs.Timeline();
      var body = new mojs.Html({
          el        : n.barDom,
          x         : {500: 0, delay: 0, duration: 500, easing: 'elastic.out'},
          isForce3d : true,
          onComplete: function () {
              promise(function(resolve) {
                  resolve();
              })
          }
      });

      var parent = new mojs.Shape({
          parent: n.barDom,
          width      : 200,
          height     : n.barDom.getBoundingClientRect().height,
          radius     : 0,
          x          : {[150]: -150},
          duration   : 1.2 * 500,
          isShowStart: true
      });

      n.barDom.style['overflow'] = 'visible';
      parent.el.style['overflow'] = 'hidden';

      var burst = new mojs.Burst({
          parent  : parent.el,
          count   : 10,
          top     : n.barDom.getBoundingClientRect().height + 75,
          degree  : 90,
          radius  : 75,
          angle   : {[-90]: 40},
          children: {
              fill     : '#EBD761',
              delay    : 'stagger(500, -50)',
              radius   : 'rand(8, 25)',
              direction: -1,
              isSwirl  : true
          }
      });

      var fadeBurst = new mojs.Burst({
          parent  : parent.el,
          count   : 2,
          degree  : 0,
          angle   : 75,
          radius  : {0: 100},
          top     : '90%',
          children: {
              fill     : '#EBD761',
              pathScale: [.65, 1],
              radius   : 'rand(12, 15)',
              direction: [-1, 1],
              delay    : .8 * 500,
              isSwirl  : true
          }
      });

      Timeline.add(body, burst, fadeBurst, parent);
      Timeline.play();
  },
  close: function (promise) {
      var n = this;
      new mojs.Html({
          el        : n.barDom,
          x         : {0: 500, delay: 10, duration: 500, easing: 'cubic.out'},
          skewY     : {0: 10, delay: 10, duration: 500, easing: 'cubic.out'},
          isForce3d : true,
          onComplete: function () {
              promise(function(resolve) {
                  resolve();
              })
          }
      }).play();
  }
}
      }).show(); 
            // $(btn).buttonLoader('stop');
          }
        });
      }
      
      
    });
    

});
