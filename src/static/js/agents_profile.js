$(document).ready( function () {
    console.log('Начали')

    $("button").click(function(){
        console.log('Нажали сохранить');

    });

    $('#save_button').on('click', '.save-button', function (){
        console.log('Нажали сохранить')
    });
});
