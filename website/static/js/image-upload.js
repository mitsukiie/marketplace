const fileInput = document.getElementById('images');
const uploadBtn = document.getElementById('upload-btn');
const preview = document.getElementById('preview');
const fileDropArea = document.getElementById('file-upload');

// Acionar o clique no input de arquivos quando o botão é clicado
uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

// Exibe pré-visualização das imagens selecionadas
fileInput.addEventListener('change', () => {
    preview.innerHTML = ''; // Limpa a pré-visualização anterior
    const files = fileInput.files;

    for (const file of files) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            preview.appendChild(img);
        }

        reader.readAsDataURL(file);
    }
});

// Permite arrastar e soltar arquivos na área de upload
fileDropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    fileDropArea.classList.add('active');
});

fileDropArea.addEventListener('dragleave', () => {
    fileDropArea.classList.remove('active');
});

fileDropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    fileDropArea.classList.remove('active');
    fileInput.files = event.dataTransfer.files;
    
    // Gera a pré-visualização das imagens
    const files = fileInput.files;
    preview.innerHTML = '';

    for (const file of files) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            preview.appendChild(img);
        }

        reader.readAsDataURL(file);
    }
});
