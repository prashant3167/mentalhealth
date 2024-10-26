import { Card } from 'react-bootstrap';

const WelcomePage = () => {

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <Card className="text-center" style={{ width: '800px', padding: '20px' }}>
        <Card.Body>
          <h2>Remote Work & Mental Health 🌍🧠</h2>
          <h4>Welcome!</h4>
          <p>If you are an employee, please wait for your company to provide you the details.</p>
          <p>
            If you are a company admin, please go to the <a href="/login">Login Page</a> to proceed.
          </p>
        </Card.Body>
      </Card>
    </div>
  );
};

export default WelcomePage;
