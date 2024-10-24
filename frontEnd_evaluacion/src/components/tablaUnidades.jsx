export function TablaUnidades({unidad}){
    return(
        <tr>
            <td>{unidad.nombre_unidad}</td>
            <td>{unidad.jefe_unidad}</td>
        </tr>
    )
}