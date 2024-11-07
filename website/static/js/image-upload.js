const fileInput = document.getElementById('images');
  const uploadBtn = document.getElementById('upload-btn');
  const preview = document.getElementById('preview');
  const fileDropArea = document.getElementById('file-upload');
  const modalImage = document.getElementById('modalImage');
  const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));

  uploadBtn.addEventListener('click', () => {
      fileInput.click();
  });

  function highlightCover() {
      const containers = preview.querySelectorAll('.preview-container');
      containers.forEach(container => container.classList.remove('cover'));

      if (containers.length > 0) {
          containers[0].classList.add('cover');
      }
  }

  function removeImage(button) {
      const container = button.closest('.preview-container');
      const checkbox = container.querySelector('.remove-image-checkbox');

      checkbox.checked = true;

      container.style.display = 'none';
      highlightCover();
  }

  // Lógica de seleção de arquivos
  fileInput.addEventListener('change', () => {
      const files = fileInput.files;

      for (const file of files) {
          const reader = new FileReader();

          reader.onload = function(event) {
              const container = document.createElement('div');
              container.classList.add('preview-container');

              const img = document.createElement('img');
              img.src = event.target.result;
              img.addEventListener('click', () => {
                  modalImage.src = img.src;
                  imageModal.show();
              });

              const removeBtn = document.createElement('button');
              removeBtn.classList.add('remove-btn');
              removeBtn.innerHTML = '&times;';
              removeBtn.addEventListener('click', () => {
                  container.remove();
                  highlightCover();
              });

              container.appendChild(img);
              container.appendChild(removeBtn);
              preview.appendChild(container);

              highlightCover();
          };

          reader.readAsDataURL(file);
      }
  });

  // Lógica de drag-and-drop
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

      const files = fileInput.files;

      for (const file of files) {
          const reader = new FileReader();

          reader.onload = function(event) {
              const container = document.createElement('div');
              container.classList.add('preview-container');

              const img = document.createElement('img');
              img.src = event.target.result;
              img.addEventListener('click', () => {
                  modalImage.src = img.src;
                  imageModal.show();
              });

              const removeBtn = document.createElement('button');
              removeBtn.classList.add('remove-btn');
              removeBtn.innerHTML = '&times;';
              removeBtn.addEventListener('click', () => {
                  container.remove();
                  highlightCover();
              });

              container.appendChild(img);
              container.appendChild(removeBtn);
              preview.appendChild(container);

              highlightCover();
          };

          reader.readAsDataURL(file);
      }
  });

  document.addEventListener('DOMContentLoaded', () => {
    const firstImage = preview.querySelector('.preview-container img');
    if (firstImage) {
        firstImage.closest('.preview-container').classList.add('cover');
    }
});