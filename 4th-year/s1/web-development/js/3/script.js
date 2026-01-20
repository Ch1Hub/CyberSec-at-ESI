const slider = document.querySelector(".slider");
const btnLeft = document.querySelector(".left");
const btnRight = document.querySelector(".right");
const animateBtn = document.getElementById("animate-btn");
const container = document.querySelector(".slider-container");

const images = [];
for (let i = 1; i <= 10; i++) {
  const img = document.createElement("img");
  img.src = `images/${i}.jpg`;
  images.push(img);
}

let startIndex = 0;


function renderImages() {
  slider.innerHTML = "";
  for (let i = 0; i < 4; i++) {
    const index = (startIndex + i) % images.length;
    slider.appendChild(images[index]);
  }
}

renderImages();


btnRight.addEventListener("click", () => {
  startIndex = (startIndex + 1) % images.length;
  renderImages();
});

btnLeft.addEventListener("click", () => {
  startIndex = (startIndex - 1 + images.length) % images.length;
  renderImages();
});



let interval;

animateBtn.addEventListener("click", () => {
  container.classList.toggle("fullscreen");

  
 

    interval = setInterval(() => {
      startIndex = (startIndex + 1) % images.length;
      renderImages();
    }, 1500);





});

