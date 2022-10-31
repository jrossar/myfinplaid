import { useState, useEffect } from 'react'
import PhoneInput from 'react-phone-number-input'

const CreateAccount = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [tel1, setTel1] = useState('');
    const [tel2, setTel2] = useState('');
    const [tel3, setTel3] = useState('');
    const [userName, setUserName] = useState('');

    const addNewUser = async (e: any) => {
        let phoneNumber = '+1' + tel1 + tel2 + tel3
        let user = { email, password, phoneNumber, userName }
        console.log(user)
        console.log(JSON.stringify(user))
        let response = await fetch('http://127.0.0.1:8000/api/create_account', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        })
    }
    return (
        <div className="createAccount">
            <form onSubmit={addNewUser}>
                <input
                    name="email"
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    required
                    type="email"
                    value={email}
                />
                <input
                    name="password"
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                    type="password"
                    value={password}
                />
                <input
                    name="username"
                    onChange={(e) => setUserName(e.target.value)}
                    placeholder="User Name"
                    required
                    type="username"
                    value={userName}
                />
                <p>(
                    <input
                        name="tel1"
                        onChange={(e) => setTel1(e.target.value)}
                        size={1}
                        required
                        placeholder='###'
                        pattern="[0-9]{3}"
                        type="tel"
                        value={tel1}
                    />
                    )
                    <input
                        name="tel2"
                        onChange={(e) => setTel2(e.target.value)}
                        size={1}
                        required
                        placeholder='###'
                        pattern="[0-9]{3}"
                        type="tel"
                        value={tel2}
                    />
                    -
                    <input
                        name="tel3"
                        onChange={(e) => setTel3(e.target.value)}
                        size={1}
                        required
                        placeholder='####'
                        pattern="[0-9]{4}"
                        type="tel"
                        value={tel3}
                    />
                </p>
                <button>Submit</button>
            </form>
        </div>
    )
}

export default CreateAccount;