import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import {PaginaUnidades} from "./pages/listaUnidades.jsx"
import {Navegacion} from "./components/navegacion.jsx"
import './App.css'

function App() {

  return (
      <BrowserRouter>
        <h1>Bienvenido</h1>
        <Navegacion />
        <Routes>
          <Route path='/unidades' element={<PaginaUnidades/>} />
        </Routes>
      </BrowserRouter>
  )
}

export default App
