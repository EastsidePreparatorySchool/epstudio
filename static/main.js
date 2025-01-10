function ImgUpload() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.click();
    fileInput.onchange = (event) => {
        const files = event.target.files;
        if (files.length > 0) {
            console.log('Selected file:', files[0].name);
            
            const exampleModal = new bootstrap.Modal(document.getElementById('exampleModal'));
            const afterUploadModal = new bootstrap.Modal(document.getElementById('afterUploadModal'));
            let nextPage = document.getElementById("exampleModal");
            let openPage = document.getElementById("afterUploadModal");
            nextPage.innerHTML = ""
            // openPage.innerHTML = "style='display: block; opacity: 100%;'"
            exampleModal.hide();

            afterUploadModal.show();
            // ResetModal();
            var loadFile = function(event) {
                var image = document.getElementById('blah');
                image.src = URL.createObjectURL(event.target.files[0]);
            };

            //v1 of showing the image
                // ResetModal();
                //var loadFile = function(event) {
                //    var image = document.getElementById('blah');
                //    image.src = URL.createObjectURL(event.target.files[0]);
                //};

            //v2 of showing the image
                const image = document.getElementById('blah');
                image.src = URL.createObjectURL(files[0]);
        }         
    }
};

function ResetModal() {
    const exampleModal = new bootstrap.Modal(document.getElementById('exampleModal'));
    exampleModal.show();
}
function PullModal(){
    const exampleModal = new bootstrap.Modal(document.getElementById('exampleModal'));
    let nextPage = document.getElementById("exampleModal");
    // nextPage.innerHTML = "style='display: block !important;'"
    exampleModal.show();
}