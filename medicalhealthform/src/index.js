import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import StarSky from 'react-star-sky';

import { BrowserRouter as Router } from 'react-router-dom';  // Import Router
const root = createRoot(document.getElementById('root'));

root.render(

    
    <Router>
      <StarSky
      isPageBackground={true}
      debugFps={false}
      frameRate={60}
      style={{ opacity: 0.9 }}
      className={''}
      starColor={'rainbow'}
      skyColor={[20, 20, 100]}
    />
    <App />
    </Router>
);
