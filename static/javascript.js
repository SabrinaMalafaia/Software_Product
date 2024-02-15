function buscarCep() {
    var cep = document.getElementById('cep').value;
    fetch('/buscar_cep', {
        method: 'POST',
        body: new URLSearchParams({
            'cep': cep
        }),
        headers: {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    })
        .then(response => response.json())
        .then(data => preencherFormulario(data))
        .catch(error => console.error('Erro ao buscar CEP:', error));
}

function preencherFormulario(data) {
    document.getElementById('logradouro').value = data.logradouro;
    document.getElementById('bairro').value = data.bairro;
    document.getElementById('cidade').value = data.localidade;
    document.getElementById('estado').value = data.uf;
}