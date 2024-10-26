import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Card, Form, Button } from "react-bootstrap";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const apiUrl = process.env.REACT_APP_API_URL;
  const handleLogin = async (e) => {
    e.preventDefault();

    const token = btoa(`${username}:${password}`);

    try {
      console.log(apiUrl);
      const response = await axios.post(
        `${apiUrl}/auth/login`,
        {},
        {
          headers: {
            Authorization: `Basic ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        localStorage.setItem("authToken", token);
        navigate("/dashboard");
      }
    } catch (error) {
      alert("Login failed: Invalid credentials.");
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-center align-items-center vh-100">
        <Card
          className="text-center"
          style={{ width: "500px", height: "300px" }}
        >
          <h1 style={{ paddingTop: "1vh" }}>Login</h1>
          <Card.Body className="d-flex justify-content-center align-items-center vh-100">
            <Form onSubmit={handleLogin}>
              <Form.Group className="mb-3" controlId="formUsername">
                <Form.Label>Username:</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-4" controlId="formPassword">
                <Form.Label>Password:</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </Form.Group>

              <div className="d-grid">
                <Button variant="primary" type="submit">
                  Login
                </Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

export default LoginPage;
