import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    axios.post('/api/login', {
      username: username,
      password: password
    })
    .then(response => {
      // Handle successful login, e.g., redirect to homepage or show a success message
      console.log("Logged in successfully:", response.data);
      // You might also want to save the user data or token to the state or local storage here
    })
    .catch(error => {
      // Handle errors, e.g., show an error message
      console.error("Error logging in:", error);
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        value={username} 
        onChange={e => setUsername(e.target.value)} 
        placeholder="Username" 
      />
      <input 
        type="password" 
        value={password} 
        onChange={e => setPassword(e.target.value)} 
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
