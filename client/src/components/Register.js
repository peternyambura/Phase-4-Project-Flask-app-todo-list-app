import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    axios.post('/api/register', {
      username: username,
      email: email,
      password: password
    })
    .then(response => {
      // Handle successful registration, e.g., redirect to login page or show a success message
      console.log("Registered successfully:", response.data);
    })
    .catch(error => {
      // Handle errors, e.g., show an error message
      console.error("Error registering:", error);
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
        type="email" 
        value={email} 
        onChange={e => setEmail(e.target.value)} 
        placeholder="Email"
      />
      <input 
        type="password" 
        value={password} 
        onChange={e => setPassword(e.target.value)} 
        placeholder="Password"
      />
      <button type="submit">Register</button>
    </form>
  );
}

export default Register;
