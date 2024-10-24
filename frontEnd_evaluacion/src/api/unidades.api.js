import axios from 'axios'

export const obtenerUnidades = () => {  
    return axios.get('http://localhost:8000/evaluacion/api/v1/evaluacion/')
}