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
function FilterModal(){
    const filterModal = new bootstrap.Modal(document.getElementById('filterModal'));
    let nextPage = document.getElementById("filterModal");
    // nextPage.innerHTML = "style='display: block !important;'"
    filterModal.show();
}
function closePopup() {
    const modal = document.getElementById("filterModal");
    if (modal) {
      const bootstrapModal = bootstrap.Modal.getInstance(modal);
      if (bootstrapModal) bootstrapModal.hide();
    }
  }

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".gal-img").forEach(img => {
        img.addEventListener("dblclick", function () {
            const creationId = this.dataset.id; // Ensure each image has a data-id attribute
            console.log("Creation ID:", creationId);
            if (creationId) {
                window.location.href = `/creation/${creationId}`;
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let currentIndex = 0;
    const images = document.querySelectorAll(".gallery img");
    const leftArrow = document.querySelector(".arrow.left");
    const rightArrow = document.querySelector(".arrow.right");

    function showImage(index) {
        images.forEach((img, i) => {
            img.classList.toggle("active", i === index);
        });
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    }

    // Attach event listeners to buttons
    leftArrow.addEventListener("click", prevImage);
    rightArrow.addEventListener("click", nextImage);

    // Ensure only the first image is visible on page load
    showImage(currentIndex);
});

function toggleFullscreen() {
    const elem = document.getElementById("galleryCarousel");
    if (document.fullscreenElement) {
      // we are in fullscreen → exit
      document.exitFullscreen();
    } else {
      // not fullscreen → request it
      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
      }
    }
}

// keep your existing fullscreenchange listener, but also update button text
document.addEventListener('fullscreenchange', () => {
const carousel = document.getElementById("galleryCarousel");
const btn = document.getElementById("fs-toggle");

if (document.fullscreenElement) {
    carousel.classList.add('fullscreen');
    btn.textContent = 'Exit Fullscreen';
} else {
    carousel.classList.remove('fullscreen');
    btn.textContent = 'Fullscreen';
}
});