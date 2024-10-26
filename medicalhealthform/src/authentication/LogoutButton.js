import { useNavigate } from 'react-router-dom';


const LogoutButton = () => {
    const navigate = useNavigate();
    const handleLogout = () => {
        localStorage.removeItem('authToken');
        navigate('/login');
      };
    return (
        <div>
          <button onClick={handleLogout}>Logout</button>
        </div>
      );
}
  
export default LogoutButton;
