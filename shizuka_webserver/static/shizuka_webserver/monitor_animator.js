$(document).ready(function() {
    var current_val = 0;
    var max_val = 0;
    var percent_val = 0;
    $('.progress-bar').each(function() {
        current_val = $(this).attr('aria-valuenow');
        max_val = $(this).attr('aria-valuemax');
        percent_val = Math.min(Math.round((current_val / max_val) * 100), 100)
        $(this).css('width', percent_val + '%')
        if(percent_val < 80){
            $(this).addClass("progress-bar-success")
        }else if(percent_val < 90 ){
            $(this).addClass("progress-bar-warning")
        }else{
            $(this).addClass("progress-bar-danger")
        }
        $(this).html(percent_val + "%")

    })
})