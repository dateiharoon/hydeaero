$('.red').change(function() {
    if($(this).is(":checked")){
    $('.green').attr('checked', false);
    }    
});

$('.green').change(function() {
    if($(this).is(":checked")){
    $('.red').attr('checked', false);
    }    
}); 
