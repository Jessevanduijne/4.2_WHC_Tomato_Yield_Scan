$('#image-selector').change(function(){
    let reader = new FileReader();
    reader.onload = function(e) {
        let dataUrl = reader.result;
        $('#selected-image').attr('src', dataUrl);
        base64Image = dataUrl.replace('data:image/jpeg;base64', '', '')
    }
    reader.readAsDataURL($('#image-selector')[0].files[0]);
});

$('#predict-button').click(function(event){
    let message = {
        image: base64Image
    }
    $.post('http://127.0.0.1:5000/predict', JSON.stringify(message), function(response){
        console.log(response);
    });
});