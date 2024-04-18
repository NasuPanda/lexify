import type { FC } from 'react';
import './App.css';
import axios from 'axios';

// Define types for the login request and response
interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

const App: FC = () => {
  // Handler function for the login button
  const handleLogin = async () => {
    const loginData: LoginRequest = {
      username: 'user@example.com',  // These should match valid credentials
      password: 'secret'
    };

    try {
      // Replace 'localhost:8000' with your backend URL if different
      const response = await axios.post<LoginResponse>('http://localhost:8000/auth/login', loginData);
      alert(`Login successful: Token - ${response.data.access_token}`);
    } catch (error: any) {
      // Handling errors and displaying a relevant message
      const errorMessage = error.response?.data?.detail || "An unexpected error occurred";
      alert(`Login failed: ${JSON.stringify(errorMessage)}`);
    }
  };

  return (
    <>
      <h1>Hello, FastAPI and React /w Docker</h1>
      <button onClick={handleLogin}>Log In</button>
    </>
  );
};

export default App;
