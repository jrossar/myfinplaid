import { Button } from "plaid-threads";
import { useState, useContext, useEffect, Component } from "react";
import { Link, useNavigate } from "react-router-dom";
import Context from './Context';
import AuthContext from "./Context/AuthContext";


const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    let loginUser = useContext(AuthContext);

    let sessionKey = 'yo';
    const state = useContext(AuthContext);

    const setSessionKey = (sk: string) => {
        console.log('inside set session key');
        sessionKey = sk;
    }

    const getSessionKey = () => {
        return sessionKey;
    }
    const dummy = () => {
        console.log('I am Dummy');
    }
    const handleSubmit = async (e: any) => {
        console.log('HELLO')
        e.preventDefault();
        const user = { email, password };
        console.log(user)
        let response = await fetch('http://127.0.0.1:8000/api/token', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });
        console.log(response);
        let data = await response.json();
        console.log(data.data['status']);
        if (data.data['status'] === 'success') {
            navigate('/myfin');
        }
        console.log('SESSION_KEY: ' + data.data['session_key']);
    }
    return (
        <div className="login">
            <form onSubmit={loginUser.loginUser} >
                <input
                    type="email"
                    name="username"
                    required
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    name="password"
                    value={password}
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button>Submit</button>
            </form>
            <Link to="/create_user">
                <button>Create Account</button>
            </Link>
            <div>
                {state.state.userEmail && <p>Hello {state.state.userEmail}</p>}
            </div>
        </div >
    );
}

export default Login;