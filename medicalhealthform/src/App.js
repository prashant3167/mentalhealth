import React from 'react';

import CheckToken from './pages/CheckToken';
import PrivateRoute from './authentication/PrivateRoute';
import { Routes, Route } from 'react-router-dom';
import LoginPage from './authentication/LoginPage';
import DashboardPage from './DashboardPage';
import CreateTokenPage from './pages/CreateToken';
import RegisterCompanyPage from './pages/RegisterCompany';
import TargetPage from './pages/TargetPage';
import WelcomePage from './pages/WelcomePage';
const App = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<WelcomePage />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <DashboardPage />
          </PrivateRoute>
        }
      />
      <Route path="/fill_form" element={<CheckToken/>}/>
      {/* <Route
        path="/fill_form"
        element={
          <PrivateRoute>
            <CheckToken />
          </PrivateRoute>
        }
      /> */}
      <Route
        path="/create_token"
        element={
          <PrivateRoute>
            <CreateTokenPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/company"
        element={
          <PrivateRoute>
            <RegisterCompanyPage />
          </PrivateRoute>
        }
      />
       <Route
        path="/target-page"
        element={
          <PrivateRoute>
            <TargetPage />
          </PrivateRoute>
        }
      />
    </Routes>
  );
};

export default App;
