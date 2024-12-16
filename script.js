document.addEventListener("DOMContentLoaded", function () {


  const form = document.getElementById('loginForm');

  form.addEventListener("submit", async function (e) {
    e.preventDefault();  // Prevent the default form submit action

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const loginData = {
      email: email,
      password: password
    };

    // Send POST request to the backend login API
    await fetch('http://127.0.0.1:8000/api/user/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Make sure Content-Type is set
      },
      body: JSON.stringify(loginData)
    })
      .then(response => response.json())
      .then(data => {
        if (data.token.access) {
          console.log(data.token.access);
          // Save the token in localStorage or sessionStorage
          localStorage.setItem('access_token', data.token.access);

          console.log('Login successful, token stored:', data.token.access);
        }
        console.log(data);
        console.log(data.token.access);

      })
      .catch(error => {
        console.error('Error:', error);
      });
  });

  let my = setInterval(() => {
    const access_token = localStorage.getItem('access_token');
    if (!access_token) {
      localStorage.clear("access_token")
      console.log('logout');
      clearInterval(my)
    }
  }, 1000);

})