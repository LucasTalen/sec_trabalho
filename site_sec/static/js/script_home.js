$(document).ready( () => {
    $('#search').on('input', function() {
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
                            $('#sugestao').append(`
                                <div class="suggestion-item">
                                    <a href="/perfil/${item.cpf}/">
                                        <span class="suggestion-name">${item.nome}</span>
                                        <span class="suggestion-cpf">${item.cpf}</span>
                                    </a>
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