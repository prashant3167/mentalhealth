import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import LogoutButton from '../authentication/LogoutButton';


const RegisterCompanyPage = () => {
  const [companyName, setCompanyName] = useState(''); 
  const [inputFields, setInputFields] = useState([{ employeeName: '' }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const apiUrl = process.env.REACT_APP_API_URL;
  const navigate = useNavigate();

  const handleCompanyOperation = async (operationType) => {
    setLoading(true);
    setError(null);
  
    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
      navigate('/login');
      return;
    }
  
    try {
      const employees = inputFields.map(field => field.employeeName);
  
      if (employees.length < 1) {
        throw new Error("Employees list is empty. At least one employee should be present.");
      }
  
      const endpoint = `${apiUrl}/register_company/${companyName}`;
      const requestConfig = {
        headers: {
          'Authorization': `Basic ${authToken}`,
          'Content-Type': 'application/json',
        },
      };
  
      let response;
  
      if (operationType === 'register') {
        response = await axios.post(endpoint, { employees }, requestConfig);
      } else if (operationType === 'addEmployee') {
        response = await axios.put(endpoint, { employees }, requestConfig);
      }
  
      const message = response.data.message || 'Operation successful!';
      setLoading(false);
      navigate(`/target-page?message=${encodeURIComponent(message)}`);
  
    } catch (error) {
      setLoading(false);
  
      if (error.response) {
        const statusCode = error.response.status;
        const errorDetail = error.response.data?.detail || 'An error occurred.';
  
        // Handle specific error types based on status code
        switch (statusCode) {
          case 400:
            setError(`Bad Request: ${errorDetail}`);
            break;
          case 401:
            setError(`Unauthorized: ${errorDetail}`);
            break;
          case 404:
            setError(`${errorDetail}`);
            break;
          case 422:
            if (errorDetail.length > 0) {
              setError(`Validation failed: ${errorDetail[0].msg}`);
            }
            else {
              setError(`Validation failed: ${errorDetail}`);
            }
            break;
          case 500:
            setError(`Internal Server Error: ${errorDetail}`);
            break;
          default:
            setError(`Error: ${errorDetail}`);
            break;
        }
  
      } else if (error.request) {
        setError('No response received from the server. Please check your internet connection or try again later.');
  
      } else {
        setError(`An unexpected error occurred: ${error.message}`);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await handleCompanyOperation('register');
  };

  const handleAddEmployee = async (e) => {
    e.preventDefault();
    await handleCompanyOperation('addEmployee');
  };

  const handleAddField = () => {
    setInputFields([...inputFields, { employeeName: '' }]);
  };

  const handleRemoveField = (index) => {
    const values = [...inputFields];
    values.splice(index, 1);
    setInputFields(values);
  };

  const handleInputChange = (index, e) => {
    const values = [...inputFields];
    values[index].employeeName = e.target.value;
    setInputFields(values);
  };

  return (
    <div className="d-flex justify-content-center flex-column align-items-center" style={{ gap: '20px' }}>
    <LogoutButton />
      <Card className="text-center" style={{ width: "500px", padding: "20px" }}>
        <h2>Register Company and Add Employees</h2>
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

          {/* Flexbox container for side-by-side buttons */}
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'space-between' }}>
            <button
              type="submit"
              disabled={loading}
              style={{ padding: '10px', width: '48%' }}  
            >
              {loading ? 'Loading...' : 'Register Company'}
            </button>

            <button
              type="button"
              onClick={handleAddEmployee}
              disabled={loading}
              style={{ padding: '10px', width: '48%' }}  
            >
              {loading ? 'Loading...' : 'Add Employee'}
            </button>
          </div>
        </form>
      </Card>

      {/* Error Message */}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {!loading && (
        <Card className="text-center" style={{ width: "500px", padding: "20px" }}>
          <h3>Add Employees</h3>
          <form>
            {inputFields.map((inputField, index) => (
              <div key={index} style={{ marginBottom: '15px', position: 'relative' }}>
                <label htmlFor={`employeeName${index}`}>Employee {index + 1} Name:</label>
                <input
                  type="text"
                  id={`employeeName${index}`}
                  value={inputField.employeeName}
                  onChange={(e) => handleInputChange(index, e)}
                  required
                  style={{ marginRight: '10px', padding: '8px', width: '80%' }}
                />
                
                <button
                  type="button"
                  onClick={() => handleRemoveField(index)}
                  style={{
                    position: 'absolute',
                    right: '5px',
                    top: '5px',
                    border: 'none',
                    background: 'transparent',
                    color: 'red',
                    fontSize: '18px',
                    cursor: 'pointer',
                  }}
                >
                  &times;
                </button>
              </div>
            ))}
            <button type="button" onClick={handleAddField} style={{ padding: '10px', width: '100%' }}>
              Add Another Employee
            </button>
          </form>
        </Card>
      )}
    </div>
  );
};

export default RegisterCompanyPage;
