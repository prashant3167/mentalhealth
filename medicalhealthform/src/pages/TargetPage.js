import { useLocation } from 'react-router-dom';
import { Card } from 'react-bootstrap';


const TargetPage = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const message = params.get('message'); // Retrieve message from query parameter
  
  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
          <Card className="text-center" style={{ width: "500px", height: "300px" }}>
            <Card.Body className="d-flex justify-content-center align-items-center vh-100">
            <Card.Title>{message ? <div>{message}</div> : "No message"}</Card.Title>
            </Card.Body>
          </Card>
        </div>
  );
};

export default TargetPage;
