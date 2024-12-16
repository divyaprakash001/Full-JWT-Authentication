const registerUser = async () => {
  const userData = {
    name: 'satya',
    email: 'newuser@gmail.com',
    tc: 'True',
    password: 'qwer1234',
    password2: 'qwer1234',
  };

  try {
    const response = await fetch('http://127.0.0.1:8000/api/user/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',  // We are sending JSON data
      },
      body: JSON.stringify(userData)  // Convert userData to JSON format
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    const data = await response.json();
    console.log('User registered successfully:', data);
  } catch (error) {
    console.error('Error during registration:', error);
  }
};

// Call the function to register
registerUser();
