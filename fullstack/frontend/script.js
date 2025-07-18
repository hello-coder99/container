fetch("/api/message")
  .then(res => res.text())
  .then(data => {
    document.getElementById("output").textContent = data;
  })
  .catch(err => {
    console.error("Error:", err);
    document.getElementById("output").textContent = "Failed to load data.";
  });

