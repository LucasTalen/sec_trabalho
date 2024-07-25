$(document).ready( () => {
    $('#search').keyup(function() {
        var query = $(this).val();

        if(query.length > 2){
            $.ajax({
                url: 'pesquisar/funcionario',
                data: {
                    'term':query
                },
                dataType: 'json',
                success: (data) => {
                    $('#sugestao').empty();
                    if(data.length){
                        data.forEach(item => {
                            $('#sugestao').append('<li>' + item + '</li>');
                        });
                    } else {
                        $('#sugestao').append('<li>Sem sugestões</li>');
                    }
                }
            });
        } else {
            $('#sugestao').empty();
        }
    });
});