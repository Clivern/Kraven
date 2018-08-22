require(['jscookie', 'toastr', 'pace', 'vue', 'axios']);

var kraven_app = kraven_app || {};


/**
 * Form to Enpoint Connect
 */
kraven_app.endpoint_connect = (function (window, document, $) {

    'use strict';

    var base = {

        el: {
            form : $("form._endpoint_connect"),
            submitButt : $("form._endpoint_connect button[type='submit']"),
        },
        actions: {
            after_success: {
                type: false,
                url: false,
                wait: false
            }

        },
        init: function(){
            if( base.el.form.length ){
                base.submit();
            }
        },
        submit : function(){
            base.el.form.on("submit", base.handler);
        },
        handler: function(event) {
            event.preventDefault();

            base.actions.after_success.type = false;
            base.actions.after_success.url = false;
            base.actions.after_success.wait = false;

            var _form = $(this);
            var _button = $(this).find("button[type='submit']");

            var afterSuccessType = _form.attr('data-succ-type');
            var afterSuccessUrl = _form.attr('data-succ-url');
            var afterSuccessWait = _form.attr('data-succ-wait');

            if (typeof afterSuccessType !== typeof undefined && afterSuccessType !== false) {
                base.actions.after_success.type = afterSuccessType;
            }
            if (typeof afterSuccessUrl !== typeof undefined && afterSuccessUrl !== false) {
                base.actions.after_success.url = afterSuccessUrl;
            }
            if (typeof afterSuccessWait !== typeof undefined && afterSuccessWait !== false) {
                base.actions.after_success.wait = afterSuccessWait;
            }

            _button.attr('disabled', 'disabled');
            _button.addClass("btn-loading");
            require(['pace'], function(Pace) {
                Pace.track(function(){
                    $.post(_form.attr('action'), base.data(_form, _button), function( response, textStatus, jqXHR ){
                        if( jqXHR.status == 200 && textStatus == 'success' ) {
                            if( response.status == "success" ){
                                base.success(response.messages, _form, _button);
                            }else{
                                base.error(response.messages, _form, _button);
                            }
                        }
                    }, 'json');
                });
            });
        },
        data : function(form, button){
            var inputs = {};
            form.serializeArray().map(function(item, index) {
                inputs[item.name] = item.value;
            });
            return inputs;
        },
        success : function(messages, form, button){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.success(messageObj.message);
                });
                break;
            }
            if( base.actions.after_success.type == "reload" ){
                if( base.actions.after_success.wait != false ){
                    setTimeout(function(){
                        location.reload();
                    }, base.actions.after_success.wait);
                }else{
                    location.reload();
                }
            }
            if( base.actions.after_success.type == "redirect" ){
                if( base.actions.after_success.wait != false ){
                    setTimeout(function(){
                        location.href = base.actions.after_success.url;
                    }, base.actions.after_success.wait);
                }else{
                    location.href = base.actions.after_success.url;
                }
            }

            if( base.actions.after_success.type == "nothing" ){
                button.removeAttr('disabled');
                button.removeClass('btn-loading');
            }
            if( base.actions.after_success.type == "reset" ){
                form[0].reset();
                button.removeAttr('disabled');
                button.removeClass('btn-loading');
            }
        },
        error : function(messages, form, button){
            button.removeAttr('disabled');
            button.removeClass('btn-loading');
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.error(messageObj.message);
                });
                break;
            }
        }
    };

   return {
        init: base.init
    };

})(window, document, jQuery);



kraven_app.profile = (function (window, document, $) {

    'use strict';

    var base = {

        el: {
            update_access_token : $("#profile_update_access_token"),
            update_refresh_token : $("#profile_update_refresh_token"),
        },
        init: function(){
            if( base.el.update_access_token.length ){
                base.el.update_access_token.find("button").on("click", function(event){
                    event.preventDefault();

                    if( !confirm(_i18n.confirm_msg) ){
                        return false;
                    }

                    var _self = $(this);
                    _self.attr('disabled', 'disabled');
                    _self.addClass("btn-loading");

                    require(['pace', 'jscookie'], function(Pace, Cookies) {
                        Pace.track(function(){
                            $.post(_self.attr('data-url'), {
                                "action": _self.attr('data-action'),
                                "token": base.el.update_access_token.find("input").val(),
                                "csrfmiddlewaretoken": Cookies.get('csrftoken')
                            }, function( response, textStatus, jqXHR ){
                                if( jqXHR.status == 200 && textStatus == 'success' ) {
                                    if( response.status == "success" ){
                                        base.success(response.messages);
                                        base.el.update_access_token.find("input").val(response.payload.token);
                                        _self.removeAttr('disabled');
                                        _self.removeClass("btn-loading");
                                    }else{
                                        base.error(response.messages);
                                        _self.removeAttr('disabled');
                                        _self.removeClass("btn-loading");
                                    }
                                }
                            }, 'json');
                        });
                    });
                })
            }
            if( base.el.update_refresh_token.length ){
                base.el.update_refresh_token.find("button").on("click", function(event){
                    event.preventDefault();

                    if( !confirm(_i18n.confirm_msg) ){
                        return false;
                    }

                    var _self = $(this);
                    _self.attr('disabled', 'disabled');
                    _self.addClass("btn-loading");

                    require(['pace', 'jscookie'], function(Pace, Cookies) {
                        Pace.track(function(){
                            $.post(_self.attr('data-url'), {
                                "action": _self.attr('data-action'),
                                "token": base.el.update_refresh_token.find("input").val(),
                                "csrfmiddlewaretoken": Cookies.get('csrftoken')
                            }, function( response, textStatus, jqXHR ){
                                if( jqXHR.status == 200 && textStatus == 'success' ) {
                                    if( response.status == "success" ){
                                        base.success(response.messages);
                                        base.el.update_refresh_token.find("input").val(response.payload.token);
                                        _self.removeAttr('disabled');
                                        _self.removeClass("btn-loading");
                                    }else{
                                        base.error(response.messages);
                                        _self.removeAttr('disabled');
                                        _self.removeClass("btn-loading");
                                    }
                                }
                            }, 'json');
                        });
                    });
                })
            }
        },
        success : function(messages){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.success(messageObj.message);
                });
                break;
            }
        },
        error : function(messages){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.error(messageObj.message);
                });
                break;
            }
        }
    };

   return {
        init: base.init
    };

})(window, document, jQuery);



/**
 * Host Endpoints
 */
kraven_app.host = (function (window, document, $) {

    'use strict';

    var base = {

        el: {
            hostName : $('form#host_create input[name="name"]'),
            hostSlug : $('form#host_create input[name="slug"]'),
            hostDelete: $('a.delete_host'),
            authSwitcher: $('form#host_create select[name="auth_type"]')
        },
        init: function(){
            if( base.el.hostName.length ){
                base.el.hostName.on("change", base.hostNameChange);
            }
            if( base.el.hostDelete.length ){
                base.el.hostDelete.on("click", base.deleteHost);
            }
            if( base.el.authSwitcher.length ){
                base.authSwitcherActionInitial();
                base.el.authSwitcher.on("change", base.authSwitcherAction);
            }
        },
        authSwitcherActionInitial: function(){
            var _self = base.el.authSwitcher;

            $('[name="tls_ca_certificate"]').closest('div.form-group').hide();
            $('[name="tls_certificate"]').closest('div.form-group').hide();
            $('[name="tls_key"]').closest('div.form-group').hide();

            if( _self.val() == "tls_server_client"){
                $('[name="tls_ca_certificate"]').closest('div.form-group').show();
                $('[name="tls_certificate"]').closest('div.form-group').show();
                $('[name="tls_key"]').closest('div.form-group').show();
            }else if( _self.val() == "tls_client_only"){
                $('[name="tls_certificate"]').closest('div.form-group').show();
                $('[name="tls_key"]').closest('div.form-group').show();
            }else if( _self.val() == "tls_server_only"){
                $('[name="tls_ca_certificate"]').closest('div.form-group').show();
            }
        },
        authSwitcherAction: function(event) {
            var _self = $(this);

            $('[name="tls_ca_certificate"]').closest('div.form-group').hide();
            $('[name="tls_certificate"]').closest('div.form-group').hide();
            $('[name="tls_key"]').closest('div.form-group').hide();

            if( _self.val() == "tls_server_client"){
                $('[name="tls_ca_certificate"]').closest('div.form-group').show();
                $('[name="tls_certificate"]').closest('div.form-group').show();
                $('[name="tls_key"]').closest('div.form-group').show();
            }else if( _self.val() == "tls_client_only"){
                $('[name="tls_certificate"]').closest('div.form-group').show();
                $('[name="tls_key"]').closest('div.form-group').show();
            }else if( _self.val() == "tls_server_only"){
                $('[name="tls_ca_certificate"]').closest('div.form-group').show();
            }
        },
        deleteHost: function(event) {
            event.preventDefault();

            if( !confirm(_i18n.confirm_msg) ){
                return false;
            }

            var _self = $(this);
            _self.attr('disabled', 'disabled');
            require(['pace', 'jscookie'], function(Pace, Cookies) {
                Pace.track(function(){
                    $.ajax({
                      method: "DELETE",
                      url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                      data: { "csrfmiddlewaretoken": Cookies.get('csrftoken') }
                    }).done(function( response ) {
                        if( response.status == "success" ){
                            base.success(response.messages);
                            _self.closest("tr").remove();
                        }else{
                            base.error(response.messages);
                        }
                    });
                });
            });
        },

        hostNameChange: function(event) {
            event.preventDefault();
            base.el.hostSlug.val(base.slugify(base.el.hostName.val()))
        },
        slugify: function(text) {
          return text.toString().toLowerCase()
            .replace(/\s+/g, '-')           // Replace spaces with -
            .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
            .replace(/\-\-+/g, '-')         // Replace multiple - with single -
            .replace(/^-+/, '')             // Trim - from start of text
            .replace(/-+$/, '');            // Trim - from end of text
        },
        success : function(messages){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.success(messageObj.message);
                });
                break;
            }
        },
        error : function(messages){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.error(messageObj.message);
                });
                break;
            }
        }
    };

   return {
        init: base.init
    };

})(window, document, jQuery);



kraven_app.host_health_check_action =  (function (window, document, $) {

    'use strict';

    var base = {

        el: {
            healthIndicator : $('[data-action="host_health_check"]')
        },
        init: function(){
            if( base.el.healthIndicator.length ){
                base.healthCheck();
            }
        },
        healthCheck: function() {
            base.el.healthIndicator.each(function( index ) {
                var _self = $(this);
                setTimeout(function(){
                    require(['pace', 'jscookie'], function(Pace, Cookies) {
                        Pace.track(function(){
                            $.ajax({
                              method: "GET",
                              url: _self.attr('data-action-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                              data: {}
                            }).done(function( response ) {
                                if( response.status == "success" ){
                                    if( response.payload.status == "up" ){
                                        _self.removeClass("btn-loading");
                                        _self.removeClass("avatar-yellow");
                                        _self.addClass("avatar-green");
                                        _self.find("i").removeClass("fe-refresh-ccw").addClass("fe-check");
                                    }else{
                                        _self.removeClass("btn-loading");
                                        _self.removeClass("avatar-yellow");
                                        _self.addClass("avatar-red");
                                        _self.find("i").removeClass("fe-refresh-ccw").addClass("fe-x");
                                    }
                                }else{
                                    _self.removeClass("btn-loading");
                                    _self.find("i").removeClass("fe-refresh-ccw").addClass("fe fe-alert-circle");
                                    base.error(response.messages);
                                }
                            });
                        });
                    });

                 }, (index + 1) * 1500, _self);
            });
        },
        success : function(messages){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.success(messageObj.message);
                });
                break;
            }
        },
        error : function(messages){
            for(var messageObj of messages) {
                require(['toastr'], function(toastr) {
                    toastr.clear();
                    toastr.error(messageObj.message);
                });
                break;
            }
        }
    };

   return {
        init: base.init
    };

})(window, document, jQuery);



kraven_app.load_tabular_data = function(Vue, axios){
    return new Vue({
        delimiters: ['${', '}'],
        el: '#app',
        data () {
            return {
                info: null,
                items: [
                    { no: '12', subject: "Carl" },
                    { no: '13', subject: "Duck" }
                ],
                isDimmerActive: true,
                errored: false
            }
        },
        mounted () {
            axios
                .get('https://api.coindesk.com/v1/bpi/currentprice.json')
                .then(response => {
                    this.info = response
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
                .finally(() => this.isDimmerActive = false)
        }
    });
}


kraven_app.notifications = function(Vue, axios){
    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_notifications',
        data () {
            return {
                notification_status: 'read',
                notifications: []
            }
        },
        mounted () {
            this.fetch();
            setInterval(function(){ this.fetch() }.bind(this), 3000)
        },
        methods:{
            fetch () {
                axios.get(app_globals.notifications_endpoint)
                    .then(response => {
                        this.notifications = response.data.payload.notifications;
                        this.notification_status = response.data.payload.status;
                    })
                    .catch(error => {
                        console.log(error)
                    })
                    .finally(() => console.log("Done!"))
            },
            mouseOver (id, delivered){
                if (delivered == false){
                    const params = new URLSearchParams();
                    params.append('notification_id', id);
                    axios({
                      method: 'post',
                      url: app_globals.notifications_endpoint,
                      data: params
                    });
                }
            }
        }
    });
}


/**
 *
 */
let hexToRgba = function(hex, opacity) {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    let rgb = result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
    return 'rgba(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ', ' + opacity + ')';
};

/**
 *
 */
$(document).ready(function() {

    $(document).ajaxStart(function() {
        require(['pace'], function(Pace) {
            Pace.restart();
        });
    });


    require(['vue', 'axios', 'jscookie'], function(Vue, axios, Cookies) {
        axios.defaults.headers.common = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken' : Cookies.get('csrftoken')
        };
        kraven_app.notifications(Vue, axios);
    });


    /** Constant div card */
    const DIV_CARD = 'div.card';

    kraven_app.endpoint_connect.init();
    kraven_app.profile.init();
    kraven_app.host.init();
    kraven_app.host_health_check_action.init();

    require(['jscookie'], function(Cookies) {
        $.ajaxSetup({
            headers:
            { 'X-CSRFToken': Cookies.get('csrftoken') }
        });
        console.log(Cookies.get('csrftoken'))
    })

    /** Initialize tooltips */
    $('[data-toggle="tooltip"]').tooltip();

    /** Initialize popovers */
    $('[data-toggle="popover"]').popover({
        html: true
    });

    /** Function for remove card */
    $('[data-toggle="card-remove"]').on('click', function(e) {
        let $card = $(this).closest(DIV_CARD);
        $card.remove();
        e.preventDefault();
        return false;
    });

    /** Function for collapse card */
    $('[data-toggle="card-collapse"]').on('click', function(e) {
        let $card = $(this).closest(DIV_CARD);
        $card.toggleClass('card-collapsed');
        e.preventDefault();
        return false;
    });

    /** Function for fullscreen card */
    $('[data-toggle="card-fullscreen"]').on('click', function(e) {
        let $card = $(this).closest(DIV_CARD);
        $card.toggleClass('card-fullscreen').removeClass('card-collapsed');
        e.preventDefault();
        return false;
    });

    /**  */
    if ($('[data-sparkline]').length) {
        let generateSparkline = function($elem, data, params) {
            $elem.sparkline(data, {
                type: $elem.attr('data-sparkline-type'),
                height: '100%',
                barColor: params.color,
                lineColor: params.color,
                fillColor: 'transparent',
                spotColor: params.color,
                spotRadius: 0,
                lineWidth: 2,
                highlightColor: hexToRgba(params.color, .6),
                highlightLineColor: '#666',
                defaultPixelsPerValue: 5
            });
        }
        require(['sparkline'], function() {
            $('[data-sparkline]').each(function() {
                let $chart = $(this);
                generateSparkline($chart, JSON.parse($chart.attr('data-sparkline')), {
                    color: $chart.attr('data-sparkline-color')
                });
            });
        });
    }

    /**  */
    if ($('.chart-circle').length) {
        require(['circle-progress'], function() {
            $('.chart-circle').each(function() {
                let $this = $(this);

                $this.circleProgress({
                    fill: {
                        color: tabler.colors[$this.attr('data-color')] || tabler.colors.blue
                    },
                    size: $this.height(),
                    startAngle: -Math.PI / 4 * 2,
                    emptyFill: '#F4F4F4',
                    lineCap: 'round'
                });
            });
        });
    }
});