let posicao_camera = 1
let cameraDisponivel;
let cameraSelecionada = 0;
let cameraLivre;
let token;
// Pede permissão para acessara câmera, ele gera um erro caso a permisão seja negada
Instascan.Camera.getCameras().then(cameras => {
    if (cameras.length > 0) {
        cameraDisponivel = cameras.filter(camera => camera.id)

        scanner.start(cameras[cameraSelecionada]);
        cameraDisponivel = cameras.filter(camera => camera.id)
        cameraLivre = cameraDisponivel.length
        
    }
});

let trocaCamera = document.getElementById("trocaCamera")
trocaCamera.addEventListener('click', () => {
    scanner.stop()
   cameraSelecionada = (cameraSelecionada + 1) % cameraLivre

    scanner.start(cameraDisponivel[cameraSelecionada]);

})





// Liga a câmera com o front-end, para a visualização do usuário
let scanner = new Instascan.Scanner({
    video: document.getElementById('preview')
});


scanner.addListener('scan', function (content) {

    verificarRota(content)
    content = ""
});

function verificarRota(content){
    const apiUrl = `/perfil/${content}/`;
    
    fetch(apiUrl, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, X-Request-Width, Content-Type, Accept'
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = `/perfil/${content}/`
        } else{
            throw new Error('Rota não encontrada.');
        }
        return response.text();
    })
    .catch(error => {
        console.error('Ocorreu um erro ao consumir a API:', error);
    });
}


//----------------------------------------------------------
















// function consumirAPI(url) {
//     const apiUrl = `https://lucas_talen_serve1.serveo.net//api/${token}/?url=${url}`;
//   // apiUrl = `https://141f1832-813e-442a-9aa8-5a9bafe2a23c-00-2fhzxziwzyf2f.riker.replit.dev/fetch_data?token=${token}&url=${url}`
//    //http://seu_ip_ou_localhost:81/fetch_data?token=seu_token_aqui&url=http://endereco_do_site_aqui

//     fetch(apiUrl, {
//         headers: {
//             'Access-Control-Allow-Origin': '*',
//             'Access-Control-Allow-Headers': 'Origin, X-Request-Width, Content-Type, Accept'
//         }
//     })
//         .then(response => response.text())
//         .then(data => {
//             if (data == "link ja foi adicionado"){
//                 alert("Esse link já foi adicionado!")
//             }else if (data == "link errado"){
//                 alert("Esse codigo QR não esta disponivel para uso!")
//             }else{
//                 console.log(data);
//                 montarTabela(data)
//             }
//         })
//         .catch(error => {
//             console.error('Ocorreu um erro ao consumir a API:', error);
//         });
// }

