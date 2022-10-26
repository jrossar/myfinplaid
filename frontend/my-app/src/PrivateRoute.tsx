import { Route } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from './Context/AuthContext';
import Login from './Login'

type PrivateRouteProps = {
    component: any,
    path: string,
    exact: boolean
}

const PrivateRoute: React.FunctionComponent<PrivateRouteProps> = ({ ...rest }) => {
    let state = useContext(AuthContext);
    return (
        state.state.userEmail ? <Route {...rest} /> : <Route path='/' />
    )
}

export default PrivateRoute;