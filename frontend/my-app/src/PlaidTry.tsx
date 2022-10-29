import { usePlaidLink } from "react-plaid-link";
import React, { useEffect, useState, useContext } from "react";
import Button from "plaid-threads/Button";
import { useNavigate } from "react-router-dom";

import Context from "./Context";
import AuthContext from "./Context/AuthContext";

const PlaidTry = () => {
    const { dispatch, sessionKey } = useContext(Context);
    const [linkToken, setLinkToken] = useState('');
    const [hi, setHi] = useState('hello');
    let user = useContext(AuthContext);
    let logoutUser = useContext(AuthContext);
    const navigate = useNavigate();

    const onSuccess = React.useCallback(
        (public_token: string) => {
            // send public_token to server
            const setToken = async () => {
                console.log('setToken');
                const response = await fetch("http://127.0.0.1:8000/api/set_access_token", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    },
                    body: JSON.stringify({
                        public_token: public_token,
                        JWT_Token: user.state.accessToken
                    }),
                    //body: JSON.stringify({
                    //    public_token: public_token,
                    //    phone_number: '+16505800752'
                    //})


                });
                const data = await response.json();
                console.log(data);
                //if (!response.ok) {
                //    console.log('Response Not Ok!');
                //    dispatch({
                //        type: "SET_STATE",
                //        state: {
                //            itemId: `no item_id retrieved`,
                //            accessToken: `no access_token retrieved`,
                //            isItemAccess: false,
                //        },
                //    });
                //    return;
                //}
                //else {
                //    console.log('Response Ok!');
                //    console.log(data);
                //    dispatch({
                //        type: "SET_STATE",
                //        state: {
                //            itemId: data.item_id,
                //            accessToken: data.access_token,
                //            isItemAccess: true,
                //        },
                //    });
                //}
            };
            setToken();
            //dispatch({ type: "SET_STATE", state: { linkSuccess: true } });
            window.history.pushState("", "", "/");
        },
        [sessionKey]
    );

    const get_transactions = async () => {
        let response = await fetch('http://127.0.0.1:8000/api/transactions', {
            method: 'POST',
            headers: {
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            body: JSON.stringify({ JWT_Token: user.state.accessToken })
        });
        let data = await response.json();
        if (!data.ok) {
            console.log('Error in get transactions');
        }
        console.log(data);
    }

    //setInterval(() => {
    //    console.log(user.refreshToken);
    //    if (user.refreshToken != '') {
    //        console.log('updating refresh token');
    //        user.updateRefreshToken('');
    //    }
    //}, 2000)

    const config: Parameters<typeof usePlaidLink>[0] = {
        token: linkToken!,
        onSuccess,
    }
    const { open, exit, ready } = usePlaidLink(config);
    useEffect(() => {
        console.log('PLAID TRY USE EFFECT');
        console.log('USER STATE');
        console.log(user.state.userEmail);
        console.log(user.state.loggedIn);
        setInterval(() => {
            //user.updateRefreshToken();
        }, 10000)
        const genToken = async () => {
            let response = await fetch('http://127.0.0.1:8000/api/create_link_token', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone_number: '+16505800752' })
            });
            let data = await response.json();
            setLinkToken(data.link_token);
            console.log(typeof dispatch);
        }
        genToken();
    }, [setLinkToken, logoutUser]);
    return (
        <div>
            <div>
                <Button type="button" large onClick={() => open()} disabled={!ready}>
                    Launch Link
                </Button>
                <a onClick={logoutUser.logoutUser}>logout</a>
                <Button onClick={get_transactions}>Get Transactions</Button>
            </div>
        </div>
    );
};

export default PlaidTry;