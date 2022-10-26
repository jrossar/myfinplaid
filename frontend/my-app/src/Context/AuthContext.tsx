import { createContext, useState, useEffect, useReducer, useDeferredValue } from 'react';
import { useInterval } from 'usehooks-ts'
import { Link, useNavigate, redirect, ActionFunction } from "react-router-dom";
import jwt_decode from "jwt-decode";
import { type } from '@testing-library/user-event/dist/type';





type AuthProviderProps = {
    children: any
}

const asyncfunc = async (e: any) => {

};

const arrowfunct = () => {

}

const initialUserState: UserState = {
    accessToken: '',
    loggedIn: false,
    refreshToken: '',
    userId: '',
    userEmail: ''
}

let user = 'None';

const userInfo = {
    accessToken: '',
    loggedIn: false,
    refreshToken: '',
    userId: '',
    userEmail: ''
}


const x: JWTToken = {
    exp: 1,
    iat: 1,
    jti: 'string',
    token_type: 'string',
    userId: 1,
    username: 'string',
}

let context = {
    loginUser: asyncfunc,
    logoutUser: arrowfunct,
    state: initialUserState,
}

interface JWTToken {
    exp: number,
    iat: number,
    jti: string,
    token_type: string,
    userId: number,
    username: string,
}



const initialState = { count: 0 }

type countState = {
    count: number
}

type countAction = {
    type: string
    payload: number
}

function reducer(state: countState, action: countAction) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + action.payload }
        case 'decrement':
            return { count: state.count - action.payload }
        default:
            return state
    }
}

type MinorAction = {
    type: string,
    payload: {}
}

type UserAction = {
    type: string,
    payload: {
        accessToken: string,
        loggedIn: boolean,
        refreshToken: string,
        userId: string,
        userEmail: string
    }
}

type UserState = {
    accessToken: string,
    loggedIn: boolean,
    refreshToken: string,
    userId: string,
    userEmail: string
}

const isUserAction = (x: any): x is UserAction => {
    if ('accessToken' in x.payload && 'loggedIn' in x.payload &&
        'refreshToken' in x.payload && 'userId' in x.payload && 'userEmail' in x.payload)
        return true;
    return false;
}

const isMinorAction = (x: any): x is MinorAction => {
    if ('type' in x && 'payload' in x) {
        return true;
    }
    return false;
}

const userReducer = (state: UserState, action: UserAction | MinorAction) => {
    switch (action.type) {
        case 'loginUser':
            if (isUserAction(action)) {
                let ret = {
                    accessToken: action.payload.accessToken,
                    loggedIn: action.payload.loggedIn,
                    refreshToken: action.payload.refreshToken,
                    userId: action.payload.userId,
                    userEmail: action.payload.userEmail
                }
                return ret as UserState;
            }
            break;
        case 'changeAccessToken':
            if (isMinorAction(action)) {
                return { ...state, accessToken: action.payload } as UserState
            }
            break;
        case 'changeLoggedIn':
            if (isMinorAction(action)) {
                return { ...state, loggedIn: action.payload } as UserState
            }
            break;
        case 'changeRefreshToken':
            if (isMinorAction(action)) {
                return { ...state, refreshToken: action.payload } as UserState
            }
            break;
        case 'changeUserEmail':
            if (isMinorAction(action)) {
                return { ...state, userEmail: action.payload } as UserState
            }
            break;
    }
    return state;
}

const AuthContext = createContext(context);
export default AuthContext;

export const AuthProvider: React.FunctionComponent<AuthProviderProps> = ({ children }) => {
    const [state, dispatch] = useReducer(userReducer, initialUserState);

    let navigate = useNavigate();

    //setInterval(() => {
    //    console.log('updateRefreshToken');
    //    updateRefreshToken();
    //}, 30000)

    useEffect(() => {
        console.log('AUTHPROVIDER USE EFFECT');
        console.log('User State!!');
        console.log(state);
    }, [state.accessToken])

    useInterval(() => {
        console.log('30000 Interval!');
        if (state.loggedIn)
            updateRefreshToken();
    }, 120000);

    let loginUser = async (e: any) => {
        console.log('Hello');
        console.log('HELLO!');
        localStorage.getItem('authTokens');
        e.preventDefault();
        let response = await fetch('http://127.0.0.1:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'email': e.target.username.value, 'password': e.target.password.value })
        });
        console.log({ 'username': e.target.username.value, 'password': e.target.password.value });
        let data = await response.json();
        console.log('data', data);
        if (response.status === 200) {
            //console.log('SetCookie!!');
            //document.cookie = 'name=Kyle';
            //console.log(document.cookie);
            var userAccessToken = jwt_decode(data.access) as JWTToken;
            //localStorage.setItem('refreshToken', data.refresh);
            //localStorage.setItem('accessToken', data.access_token);
            console.log('STATE!!');
            console.log(state);
            console.log('Dispatch Login User!!!');
            dispatch({
                type: 'loginUser', payload: {
                    accessToken: data.access,
                    loggedIn: true,
                    refreshToken: data.refresh,
                    userId: userAccessToken.userId,
                    userEmail: userAccessToken.username
                }
            });
            console.log('Dispatch Finished!!!');
            navigate('/plaidtry');
        } else {
            alert('Something went wrong!')
        }
    }

    let logoutUser = () => {
        console.log('Logging Out User');
        localStorage.removeItem('authTokens');
        navigate('/');
    }

    let updateRefreshToken = async () => {
        let response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'refresh': state.refreshToken })
        });
        let data = await response.json();
        console.log('DATA!!');
        console.log(data);
        console.log('setting refresh token!');
        dispatch({ type: 'changeRefreshToken', payload: data.refresh });
        //localStorage.setItem('refreshToken', data.refresh)
        //localStorage.setItem('accessToken', data.access)
    }

    let contextData = {
        loginUser: loginUser,
        logoutUser: logoutUser,
        state: state
    }

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider >
    )
}