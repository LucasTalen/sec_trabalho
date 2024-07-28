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
                            $('#sugestao').html(`
                                <div class="suggestion-item">
                                    <span class="suggestion-name">${item.nome}</span>
                                    <span class="suggestion-cpf">${item.cpf}</span>
                                </div>`
                            );
                        });
                    } else {
                        $('#sugestao').append('Sem sugestões');
                    }
                }
            });
        } else {
            $('#sugestao').empty();
        }
    });
});