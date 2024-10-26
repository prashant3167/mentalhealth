import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LogoutButton from './authentication/LogoutButton'
import { Card } from 'react-bootstrap';


const DashboardPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const authToken = localStorage.getItem('authToken');
      if (!authToken) {
        navigate('/login');
        return;
      }
    };

    fetchData();
  }, [navigate]);


  // Function to handle redirect to "Register Company" page
  const redirectToRegisterCompany = () => {
    navigate('/company');
  };

  // Function to handle redirect to "Create Token" page
  const redirectToCreateToken = () => {
    navigate('/create_token');
  };

  return (
    <div className="d-flex justify-content-center flex-column align-items-center" style={{ gap: '20px' }}>
    {/* Logout Button */}
    <LogoutButton />

    {/* Card with Dashboard content */}
    <Card className="text-center" style={{ width: "500px", padding: "30px", borderRadius: '10px' }}>
      <h2 style={{ marginBottom: '20px', fontSize: '2rem' }}>Dashboard</h2>

      {/* Buttons with custom styling */}
      <button
        onClick={redirectToRegisterCompany}
        className="btn btn-primary mb-3"
        style={{ width: '100%', padding: '12px', borderRadius: '5px' }}
      >
        Register Company/Add Employee
      </button>
      
      <button
        onClick={redirectToCreateToken}
        className="btn btn-secondary"
        style={{ width: '100%', padding: '12px', borderRadius: '5px' }}
      >
        Create Token
      </button>
    </Card>
  </div>
  );
};

export default DashboardPage;
