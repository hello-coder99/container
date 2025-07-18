fetch('/api/message')
     .then(response => response.json())
     .then(data => {
       document.getElementById('output').innerText = data.message;
     })
     .catch(error => {
       document.getElementById('output').innerText = 'Error: ' + error;
     });
