
    const title = document.getElementById("title");

    const checkboxes = {
      bold: document.getElementById("bold"),
      italic: document.getElementById("italic"),
      red: document.getElementById("red"),
      big: document.getElementById("big")
    };


    function updateStyles() {
      title.classList.toggle("bold", checkboxes.bold.checked);
      title.classList.toggle("italic", checkboxes.italic.checked);
      title.classList.toggle("red", checkboxes.red.checked);
      title.classList.toggle("big", checkboxes.big.checked);
    }


    Object.values(checkboxes).forEach(box => {
      box.addEventListener("change", updateStyles);
    });
