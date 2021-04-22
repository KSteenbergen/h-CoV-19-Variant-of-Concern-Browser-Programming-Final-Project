// run our javascript once the page is ready
$(document).ready(function(){
    $( "#accordion" ).accordion({
        collapsible: true,
        active: false,
        animate: 500,
        heightStyle: "content",
        header: ".header"
    }); 
    $(".widget").checkboxradio({
        icon: false
    })
});