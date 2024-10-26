import React from "react";
import { useLocation } from "react-router-dom";
import { Card } from "react-bootstrap";
import MedicalHealthForm from "./MedicalHealthForm"; 

const CheckToken = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const token = queryParams.get("token");

  return (
    <div>
      {token ? (
        <MedicalHealthForm />
      ) : (
        <div className="d-flex justify-content-center align-items-center vh-100">
          <Card className="text-center" style={{ width: "500px", height: "300px" }}>
            <Card.Body className="d-flex justify-content-center align-items-center vh-100">
              <Card.Title>No Form Present for you</Card.Title>
            </Card.Body>
          </Card>
        </div>
      )}
    </div>
  );
};

export default CheckToken;
