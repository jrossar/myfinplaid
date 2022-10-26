import React from 'react';
import logo from './logo.svg';
import './App.css';
import { AuthProvider } from './Context/AuthContext';
import { Router, Route, Link } from 'react-router-dom';
import PlaidTry from './PlaidTry';
import Login from './Login';
import MyFin from './MyFin';
import PrivateRoute from './PrivateRoute'

function App() {
  return (
    <div className='App'>
      <AuthProvider>
        <Login />
        <PlaidTry />
      </AuthProvider>
    </div>
  )
}

export default App;
