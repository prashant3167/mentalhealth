import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import LogoutButton from '../authentication/LogoutButton';

const CreateTokenPage = () => {
  const [companyName, setCompanyName] = useState(''); // To store company name from the form
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const apiUrl = process.env.REACT_APP_API_URL;
  const navigate = useNavigate();
  const baseUrl = window.location.origin;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
      navigate('/login'); 
      return;
    }

    try {
      const response = await axios.post(`${apiUrl}/create_token/${companyName}`, {}, {
        headers: {
          'Authorization': `Basic ${authToken}`, // Assuming basic auth
          'Content-Type': 'application/json',
        },
      });
      setTokens(response.data.tokens || []);
      setLoading(false);
    } catch (error) {
        if (error.response) {
            setError(error.response.data?.detail || 'Failed to fetch tokens.');
          } else if (error.request) {
            setError('No response received from the server.');
          } else {
            setError('An error occurred.');
          }
      setLoading(false);
    }
  };

  return (
    
    <div className="d-flex justify-content-center flex-column align-items-center" style={{ gap: '20px' }}>
      <LogoutButton />
      {/* First Card for Form */}
      <Card className="text-center" style={{ width: "500px", padding: "20px" }}>
        <h2>Create Token and Display Data</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="companyName">Enter Company Name:</label>
            <input
              type="text"
              id="companyName"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              required
              style={{ marginBottom: '10px', padding: '8px', width: '100%' }}
            />
          </div>
          <button type="submit" disabled={loading} style={{ padding: '10px', width: '100%' }}>
            {loading ? 'Loading...' : 'Fetch Tokens'}
          </button>
        </form>
        <div>
            <p>Please ask your employees to use a token like this:</p>
            <p>{baseUrl}/fill_form?token=individual_token</p>
            <p>For example, if Andy has token e6c400a56665cc3a, the link will be:</p>
            <strong>{`${baseUrl}/fill_form?token=e6c400a56665cc3a`}</strong>
            </div>
      </Card>

      {error && <div style={{ color: 'red' }}>{error}</div>}
      
      {!loading && tokens.length > 0 && (
        <Card className="text-center" style={{ width: "500px", padding: "20px" }}>
          <table border="1" cellPadding="10" style={{ width: '100%', marginTop: '10px' }}>
            <thead>
              <tr>
                <th>Employee</th>
                <th>Token</th>
              </tr>
            </thead>
            <tbody>
              {tokens.map((token, index) => (
                <tr key={index}>
                  <td>{token.employee}</td>
                  <td>{token.token}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}
    </div>
  );
};

export default CreateTokenPage;
