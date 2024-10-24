import {Link} from 'react-router-dom'

export function Navegacion() {
    return(
        <div>
            <Link to="/">Evaluacion</Link>
            <Link to="/unidades">Ver unidades</Link>
        </div>
    )
}