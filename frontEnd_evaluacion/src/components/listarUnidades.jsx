import {obtenerUnidades} from "../api/unidades.api"
import {useEffect, useState} from 'react'
import {TablaUnidades} from './tablaUnidades'

export function ListarUnidades() {
    const  [unidades, setUnidades] = useState([]);

    useEffect(()=> {
        async function cargarUnidades(){
            const res = await obtenerUnidades();
            setUnidades(res.data)
        }
        cargarUnidades();
    }, [])

    return(
        <div>{
            <table border={1}>
                <thead>
                    <th>Unidad</th>
                    <th>Jefe</th>
                </thead>
                <tbody>{
                unidades.map(unidad => (
                    <TablaUnidades key={unidad.id_unidad} unidad={unidad}/>
                ))}
                </tbody>
            </table>
        }</div>
    )
}