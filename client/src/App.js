import React from 'react';
import { BrowserRouter as Router, useRoutes, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import TablePage from './pages/TablePage';
import { NextUIProvider } from '@nextui-org/react';

// 定义路由
const AppRoutes = () => {
  let routes = useRoutes([
    { path: '/login', element: <LoginPage /> },
    { path: '/table', element: <TablePage /> },
    { path: '/', element: <Navigate to="/login" replace /> }
  ]);

  return routes;
};

const App = () => {
  return (
    <NextUIProvider>
      <Router>
        <AppRoutes />
      </Router>
    </NextUIProvider>
  );
};

export default App;

