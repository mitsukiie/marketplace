function previewImage(event, previewId) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById(previewId);
        if (output) {
            output.src = reader.result;
        }
    };
    reader.readAsDataURL(event.target.files[0]);
}
